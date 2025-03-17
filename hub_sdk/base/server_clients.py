# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import os
import signal
import sys
from pathlib import Path
from time import sleep
from typing import Any, Dict, Optional

from requests import Response

from hub_sdk.base.api_client import APIClient
from hub_sdk.config import HUB_API_ROOT
from hub_sdk.helpers.utils import threaded


def is_colab():
    """
    Check if the current script is running inside a Google Colab notebook.

    Returns:
        (bool): True if running inside a Colab notebook, False otherwise.
    """
    return "COLAB_RELEASE_TAG" in os.environ or "COLAB_BACKEND_VERSION" in os.environ


__version__ = sys.version.split()[0]

AGENT_NAME = f"python-{__version__}-colab" if is_colab() else f"python-{__version__}-local"


class ModelUpload(APIClient):
    """
    Manages uploading and exporting model files and metrics to Ultralytics HUB and heartbeat updates.

    This class handles the communication with Ultralytics HUB API for model-related operations including
    uploading model checkpoints, metrics, exporting models to different formats, and maintaining heartbeat
    connections to track model training status.

    Attributes:
        name (str): Identifier for the model upload instance.
        alive (bool): Flag indicating if the heartbeat thread should continue running.
        agent_id (str): Unique identifier for the agent sending heartbeats.
        rate_limits (Dict): Dictionary containing rate limits for different API operations in seconds.
    """

    def __init__(self, headers):
        """
        Initialize ModelUpload with API client configuration.

        Args:
            headers (Dict): HTTP headers to use for API requests.
        """
        super().__init__(f"{HUB_API_ROOT}/v1/models", headers)
        self.name = "model"
        self.alive = True
        self.agent_id = None
        self.rate_limits = {"metrics": 3.0, "ckpt": 900.0, "heartbeat": 300.0}

    def upload_model(self, id, epoch, weights, is_best=False, map=0.0, final=False):
        """
        Upload a model checkpoint to Ultralytics HUB.

        Args:
            id (str): The unique identifier of the model.
            epoch (int): The current training epoch.
            weights (str): Path to the model weights file.
            is_best (bool): Indicates if the current model is the best one so far.
            map (float): Mean average precision of the model.
            final (bool): Indicates if the model is the final model after training.

        Returns:
            (Optional[Response]): Response object from the upload request, or None if it fails.
        """
        try:
            # Determine the correct file path
            weights_path = weights if os.path.isabs(weights) else os.path.join(os.getcwd(), weights)

            # Check if the file exists
            if not Path(weights_path).is_file():
                raise FileNotFoundError(f"File not found: {weights_path}")

            with open(weights_path, "rb") as f:
                file = f.read()

            # Prepare the endpoint and data
            endpoint = f"/{id}/upload"
            data = {"epoch": epoch, "type": "final" if final else "epoch"}
            files = {"best.pt": file} if final else {"last.pt": file}
            if final:
                data["map"] = map
            else:
                data["isBest"] = bool(is_best)

            # Perform the POST request
            response = self.post(endpoint, data=data, files=files, stream=True)

            # Log the appropriate message
            msg = "Model optimized weights uploaded." if final else "Model checkpoint weights uploaded."
            self.logger.debug(msg)
            return response
        except Exception as e:
            self.logger.error(f"Failed to upload file for {self.name}: {e}")

    def upload_metrics(self, id: str, data: dict) -> Optional[Response]:
        """
        Upload metrics data for a specific model.

        Args:
            id (str): The unique identifier of the model to which the metrics are being uploaded.
            data (dict): The metrics data to upload.

        Returns:
            (Optional[Response]): Response object from the upload_metrics request, or None if it fails.
        """
        try:
            payload = {"metrics": data, "type": "metrics"}
            endpoint = f"{HUB_API_ROOT}/v1/models/{id}"
            r = self.post(endpoint, json=payload)
            self.logger.debug("Model metrics uploaded.")
            return r
        except Exception as e:
            self.logger.error(f"Failed to upload metrics for Model({id}): {e}")

    def export(self, id: str, format: str) -> Optional[Response]:
        """
        Export a model to a specific format.

        Args:
            id (str): The unique identifier of the model to be exported.
            format (str): The format to export the model to.

        Returns:
            (Optional[Response]): Response object from the export request, or None if it fails.
        """
        try:
            payload = {"format": format}
            endpoint = f"/{id}/export"
            return self.post(endpoint, json=payload)
        except Exception as e:
            self.logger.error(f"Failed to export file for Model({id}): {e}")

    @threaded
    def _start_heartbeats(self, model_id: str, interval: int) -> None:
        """
        Begin a threaded heartbeat loop to report the agent's status to Ultralytics HUB.

        This method initiates a threaded loop that periodically sends heartbeats to Ultralytics HUB
        to report the status of the agent. Heartbeats are sent at regular intervals as defined in the
        'rate_limits' dictionary.

        Args:
            model_id (str): The unique identifier of the model associated with the agent.
            interval (int): The time interval, in seconds, between consecutive heartbeats.
        """
        endpoint = f"{HUB_API_ROOT}/v1/agent/heartbeat/models/{model_id}"
        try:
            self.logger.debug(f"Heartbeats started at {interval}s interval.")
            while self.alive:
                payload = {
                    "agent": AGENT_NAME,
                    "agentId": self.agent_id,
                }
                res = self.post(endpoint, json=payload).json()
                new_agent_id = res.get("data", {}).get("agentId")

                self.logger.debug("Heartbeat sent.")

                # Update the agent id as requested by the server
                if new_agent_id != self.agent_id:
                    self.logger.debug("Agent Id updated.")
                    self.agent_id = new_agent_id
                sleep(interval)
        except Exception as e:
            self.logger.error(f"Failed to start heartbeats: {e}")
            raise e

    def _stop_heartbeats(self) -> None:
        """
        Stop the threaded heartbeat loop.

        This method stops the threaded loop responsible for sending heartbeats to Ultralytics HUB. It sets the 'alive'
        flag to False, which will cause the loop in '_start_heartbeats' to exit.
        """
        self.alive = False
        self.logger.debug("Heartbeats stopped.")

    def _register_signal_handlers(self) -> None:
        """Register signal handlers for SIGTERM and SIGINT signals to gracefully handle termination."""
        signal.signal(signal.SIGTERM, self._handle_signal)  # Polite request to terminate
        signal.signal(signal.SIGINT, self._handle_signal)  # CTRL + C

    def _handle_signal(self, signum: int, frame: Any) -> None:
        """
        Handle kill signals and prevent heartbeats from being sent on Colab after termination.

        Args:
            signum (int): Signal number.
            frame (Any): The current stack frame (not used in this method).
        """
        self.logger.debug("Kill signal received!")
        self._stop_heartbeats()
        sys.exit(signum)

    def predict(self, id: str, image: str, config: Dict[str, Any]) -> Optional[Response]:
        """
        Perform a prediction using the specified image and configuration.

        Args:
            id (str): Unique identifier for the model to use for prediction.
            image (str): Image path for prediction.
            config (Dict[str, Any]): Configuration parameters for the prediction.

        Returns:
            (Optional[Response]): Response object from the predict request, or None if upload fails.
        """
        try:
            base_path = os.getcwd()
            image_path = os.path.join(base_path, image)

            if not os.path.isfile(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            with open(image_path, "rb") as f:
                image_file = f.read()

            files = {"image": image_file}
            endpoint = f"{HUB_API_ROOT}/v1/predict/{id}"
            return self.post(endpoint, files=files, data=config)

        except Exception as e:
            self.logger.error(f"Failed to predict for Model({id}): {e}")


class ProjectUpload(APIClient):
    """
    Handle project file uploads to Ultralytics HUB via API requests.

    This class manages the uploading of project-related files to Ultralytics HUB, providing
    methods to handle image uploads for projects.

    Attributes:
        name (str): Identifier for the project upload instance.
    """

    def __init__(self, headers: dict):
        """
        Initialize the class with the specified headers.

        Args:
            headers (dict): The headers to use for API requests.
        """
        super().__init__(f"{HUB_API_ROOT}/v1/projects", headers)
        self.name = "project"

    def upload_image(self, id: str, file: str) -> Optional[Response]:
        """
        Upload a project image to the hub.

        Args:
            id (str): The ID of the project to upload the image to.
            file (str): The path to the image file to upload.

        Returns:
            (Optional[Response]): Response object from the upload image request, or None if it fails.
        """
        base_path = os.getcwd()
        file_path = os.path.join(base_path, file)
        file_name = os.path.basename(file_path)

        with open(file_path, "rb") as image_file:
            project_image = image_file.read()
        try:
            files = {"file": (file_name, project_image)}
            endpoint = f"/{id}/upload"
            r = self.post(endpoint, files=files)
            self.logger.debug("Project Image uploaded successfully.")
            return r
        except Exception as e:
            self.logger.error(f"Failed to upload image for {self.name}({id}): {str(e)}")


class DatasetUpload(APIClient):
    """
    Manages uploading dataset files to Ultralytics HUB via API requests.

    This class handles the uploading of dataset files to Ultralytics HUB, providing methods
    to manage dataset uploads.

    Attributes:
        name (str): Identifier for the dataset upload instance.
    """

    def __init__(self, headers: dict):
        """
        Initialize the class with the specified headers.

        Args:
            headers (dict): The headers to use for API requests.
        """
        super().__init__(f"{HUB_API_ROOT}/v1/datasets", headers)
        self.name = "dataset"

    def upload_dataset(self, id, file) -> Optional[Response]:
        """
        Upload a dataset file to the hub.

        Args:
            id (str): The ID of the dataset to upload.
            file (str): The path to the dataset file to upload.

        Returns:
            (Optional[Response]): Response object from the upload dataset request, or None if it fails.
        """
        try:
            if Path(f"{file}").is_file():
                with open(file, "rb") as f:
                    dataset_file = f.read()
                endpoint = f"/{id}/upload"
                filename = file.split("/")[-1]
                files = {filename: dataset_file}
                r = self.post(endpoint, files=files, stream=True)
                self.logger.debug("Dataset uploaded successfully.")
                return r
        except Exception as e:
            self.logger.error(f"Failed to upload dataset for {self.name}({id}): {str(e)}")
