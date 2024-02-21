# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import os
import platform
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
    """Check if the current environment is Google Colab."""
    return "google.colab" in platform.sys.modules


__version__ = sys.version.split()[0]

AGENT_NAME = f"python-{__version__}-colab" if is_colab() else f"python-{__version__}-local"


class ModelUpload(APIClient):
    def __init__(self, headers):
        """Initialize ModelUpload with API client configuration."""
        super().__init__(f"{HUB_API_ROOT}/v1/models", headers)
        self.name = "model"
        self.alive = True
        self.agent_id = None
        self.rate_limits = {"metrics": 3.0, "ckpt": 900.0, "heartbeat": 300.0}

    def upload_model(self, id, epoch, weights, is_best=False, map=0.0, final=False):
        """
        Upload a model checkpoint to Ultralytics HUB.

        Args:
            epoch (int): The current training epoch.
            weights (str): Path to the model weights file.
            is_best (bool): Indicates if the current model is the best one so far.
            map (float): Mean average precision of the model.
            final (bool): Indicates if the model is the final model after training.
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
        Upload a file for a specific entity.

        Args:
            id (str): The unique identifier of the entity to which the file is being uploaded.
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
            self.logger.error(f"Failed to upload metrics for Model({id}): %s", e)

    def export(self, id: str, format: str) -> Optional[Response]:
        """
        Export a file for a specific entity.

        Args:
            id (str): The unique identifier of the entity to which the file is being exported.
            format (str): Path to the file to be Exported.

        Returns:
            (Optional[Response]): Response object from the export request, or None if it fails.
        """
        try:
            payload = {"format": format}
            endpoint = f"/{id}/export"
            return self.post(endpoint, json=payload)
        except Exception as e:
            self.logger.error(f"Failed to export file for Model({id}): %s", e)

    @threaded
    def _start_heartbeats(self, model_id: str, interval: int) -> None:
        """
        Begin a threaded heartbeat loop to report the agent's status to Ultralytics HUB.

        This method initiates a threaded loop that periodically sends heartbeats to the Ultralytics HUB
        to report the status of the agent. Heartbeats are sent at regular intervals as defined in the
        'rate_limits' dictionary.

        Args:
            model_id (str): The unique identifier of the model associated with the agent.
            interval (int): The time interval, in seconds, between consecutive heartbeats.

        Returns:
            (None): The method does not return a value.
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

        This method stops the threaded loop responsible for sending heartbeats to the Ultralytics HUB.
        It sets the 'alive' flag to False, which will cause the loop in '_start_heartbeats' to exit.

        Returns:
            (None): The method does not return a value.
        """
        self.alive = False
        self.logger.debug("Heartbeats stopped.")

    def _register_signal_handlers(self) -> None:
        """
        Register signal handlers for SIGTERM and SIGINT signals to gracefully handle termination.

        Returns:
            (None): The method does not return a value.
        """
        signal.signal(signal.SIGTERM, self._handle_signal)  # Polite request to terminate
        signal.signal(signal.SIGINT, self._handle_signal)  # CTRL + C

    def _handle_signal(self, signum: int, frame: Any) -> None:
        """
        Handle kill signals and prevent heartbeats from being sent on Colab after termination.

        This method does not use frame, it is included as it is passed by signal.

        Args:
            signum (int): Signal number.
            frame: The current stack frame (not used in this method).

        Returns:
            (None): The method does not return a value.
        """
        self.logger.debug("Kill signal received!")
        self._stop_heartbeats()
        sys.exit(signum)

    def predict(self, id: str, image: str, config: Dict[str, Any]) -> Optional[Response]:
        """
        Perform a prediction using the specified image and configuration.

        Args:
            id (str): Unique identifier for the prediction request.
            image (str): Image path for prediction.
            config (dict): Configuration parameters for the prediction.

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
            self.logger.error(f"Failed to predict for Model({id}): %s", e)


class ProjectUpload(APIClient):
    def __init__(self, headers: dict):
        """
        Initialize the class with the specified headers.

        Args:
            headers: The headers to use for API requests.
        """
        super().__init__(f"{HUB_API_ROOT}/v1/projects", headers)
        self.name = "project"

    def upload_image(self, id: str, file: str) -> Optional[Response]:
        """
        Upload a project file to the hub.

        Args:
            id (str): The ID of the dataset to upload.
            file (str): The path to the dataset file to upload.

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
    def __init__(self, headers: dict):
        """
        Initialize the class with the specified headers.

        Args:
            headers: The headers to use for API requests.
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
