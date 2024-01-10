import os
import platform
import signal
import sys
from pathlib import Path
from time import sleep

from hub_sdk.base.api_client import APIClient
from hub_sdk.config import HUB_API_ROOT
from hub_sdk.helpers.utils import threaded


def is_colab():
    return "google.colab" in platform.sys.modules


__version__ = sys.version.split()[0]

AGENT_NAME = f"python-{__version__}-colab" if is_colab() else f"python-{__version__}-local"


class ModelUpload(APIClient):
    def __init__(self, headers):
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
            if Path(weights_path).is_file():
                with open(weights_path, "rb") as f:
                    file = f.read()

                # Prepare the endpoint and data
                endpoint = f"/{id}/upload"
                data = {"epoch": epoch, "type": "final" if final else "epoch"}
                files = {"best.pt": file} if final else {"last.pt": file}
                if final:
                    data.update({"map": map})
                else:
                    data.update({"isBest": bool(is_best)})

                # Perform the POST request
                response = self.post(endpoint, data=data, files=files)

                # Log the appropriate message
                msg = "Model optimized weights uploaded." if final else "Model checkpoint weights uploaded."
                self.logger.debug(msg)
                return response
            else:
                raise FileNotFoundError(f"File not found: {weights_path}")

        except Exception as e:
            self.logger.error(f"Failed to upload file for {self.name}: {e}")
            raise

    def upload_metrics(self, id: str, data: dict):
        """
        Upload a file for a specific entity.

        Args:
            id (str): The unique identifier of the entity to which the file is being uploaded.
            file (str): Path to the file to be uploaded.

        Returns:
            dict or None: Response data if successful, None on failure.
        """
        try:
            payload = {"metrics": data, "type": "metrics"}
            endpoint = f"{HUB_API_ROOT}/v1/models/{id}"
            r = self.post(endpoint, json=payload)
            self.logger.debug("Model metrics uploaded.")
            return r
        except Exception as e:
            self.logger.error(f"Failed to upload file for {self.name}: %s", e)
            raise e

    def export(self, id, format):
        """
        Export a file for a specific entity.

        Args:
            id (str): The unique identifier of the entity to which the file is being exported.
            format (str): Path to the file to be Exported.

        Returns:
            dict or None: Response data if successful, None on failure.
        """
        try:
            payload = {"format": format}
            endpoint = f"/{id}/export"
            return self.post(endpoint, json=payload)
        except Exception as e:
            self.logger.error(f"Failed to export file for {self.name}: %s", e)
            raise e

    @threaded
    def _start_heartbeats(self, model_id: str, interval: dict):
        """
        Begin a threaded heartbeat loop to report the agent's status to Ultralytics HUB.

        This method initiates a threaded loop that periodically sends heartbeats to the Ultralytics HUB
        to report the status of the agent. Heartbeats are sent at regular intervals as defined in the
        'rate_limits' dictionary.

        Parameters:
            model_id (str): The unique identifier of the model associated with the agent.

        Returns:
            None
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
            None
        """
        self.alive = False
        self.logger.debug("Heartbeats stopped.")

    def _register_signal_handlers(self) -> None:
        """Register signal handlers for SIGTERM and SIGINT signals to gracefully handle termination."""
        signal.signal(signal.SIGTERM, self._handle_signal)  # Polite request to terminate
        signal.signal(signal.SIGINT, self._handle_signal)  # CTRL + C

    def _handle_signal(self, signum, frame) -> None:
        """
        Handle kill signals and prevent heartbeats from being sent on Colab after termination.

        This method does not use frame, it is included as it is passed by signal.
        """
        self.logger.debug("Kill signal received!")
        self._stop_heartbeats()
        sys.exit(signum)

    def predict(self, id, image, config):
        """
        Perform a prediction using the specified image and configuration.

        :param id: The identifier for the prediction.
        :param image: The path to the image file.
        :param config: A configuration for the prediction (JSON).
        :return: The prediction result (response from self.post).
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
            self.logger.error(f"Failed to predict for {self.name}: %s", e)
            raise e


class ProjectUpload(APIClient):
    def __init__(self, headers):
        """
        Initialize the class with the specified headers.

        Args:
            headers: The headers to use for API requests.
        """
        super().__init__(f"{HUB_API_ROOT}/v1/projects", headers)
        self.name = "project"

    def upload_image(self, id: str, file):
        """
        Upload a project file to the hub.

        Args:
            id (YourIdType): The ID of the dataset to upload.
            file (str): The path to the dataset file to upload.
        Returns:
            Any: The response from the upload request.
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
            self.logger.error("Failed to upload image for %s: %s", self.name, str(e))
            raise e


class DatasetUpload(APIClient):
    def __init__(self, headers):
        """
        Initialize the class with the specified headers.

        Args:
            headers: The headers to use for API requests.
        """
        super().__init__(f"{HUB_API_ROOT}/v1/datasets", headers)
        self.name = "dataset"

    def upload_dataset(self, id, file):
        """
        Upload a dataset file to the hub.

        Args:
            id (YourIdType): The ID of the dataset to upload.
            file (str): The path to the dataset file to upload.

        Returns:
            Any: The response from the upload request.
        """
        try:
            if Path(f"{file}").is_file():
                with open(file, "rb") as f:
                    dataset_file = f.read()
                endpoint = f"/{id}/upload"
                filename = file.split("/")[-1]
                files = {filename: dataset_file}
                r = self.post(endpoint, files=files)
                self.logger.debug("Dataset uploaded successfully.")
                return r
        except Exception as e:
            self.logger.error(f"Failed to upload dataset for {self.name}: %s", e)
            raise e
