# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

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

    Example:
        ```python
        if is_colab():
            print("Running in Google Colab")
        ```
    """
    return "COLAB_RELEASE_TAG" in os.environ or "COLAB_BACKEND_VERSION" in os.environ


__version__ = sys.version.split()[0]

AGENT_NAME = f"python-{__version__}-colab" if is_colab() else f"python-{__version__}-local"


class ModelUpload(APIClient):
    """
    ModelUpload class for managing model uploads and interactions with the Ultralytics HUB API.

    This class extends the APIClient to provide functionality for uploading model weights, exporting models,
    uploading metrics, and managing heartbeats to the Ultralytics HUB. It contains methods for interacting
    with the Ultralytics backend to manage model lifecycle events.

    Attributes:
        name (str): The default name assigned to the models.
        alive (bool): A flag indicating whether the agent is active for sending heartbeats.
        agent_id (Optional[str]): The unique identifier for the agent sending heartbeats.
        rate_limits (dict): A dictionary storing rate limits for various activities like 'metrics', 'ckpt', and 'heartbeat'.

    Methods:
        upload_model(id, epoch, weights, is_best=False, map=0.0, final=False):
            Upload a model checkpoint to the Ultralytics HUB.

        upload_metrics(id: str, data: dict) -> Optional[Response]:
            Upload a file containing metrics for a specific entity.

        export(id: str, format: str) -> Optional[Response]:
            Export a model file for a specific entity.

        predict(id: str, image: str, config: Dict[str, Any]) -> Optional[Response]:
            Perform a prediction using the specified image and configuration.

        _start_heartbeats(model_id: str, interval: int) -> None:
            Begin a threaded heartbeat loop to report the agent's status to Ultralytics HUB.

        _stop_heartbeats() -> None:
            Stop the threaded heartbeat loop.

        _register_signal_handlers() -> None:
            Register signal handlers for SIGTERM and SIGINT.

        _handle_signal(signum: int, frame: Any) -> None:
            Handle kill signals and prevent heartbeats from being sent on termination.

    References:
        - [Requests: HTTP for Humans](https://docs.python-requests.org/en/master/)
        - [Python Signal Module](https://docs.python.org/3/library/signal.html)

    Example:
        ```python
        headers = {"Authorization": "Bearer YOUR_API_KEY"}
        model_uploader = ModelUpload(headers=headers)
        model_uploader.upload_model(
            id="abcdef",
            epoch=5,
            weights="/path/to/weights.pt",
            is_best=True,
            map=0.85,
            final=True
        )
        ```
    """

    def __init__(self, headers):
        """
        Initialize ModelUpload with API client configuration.

        Args:
            headers (dict): HTTP headers required for API requests.

        Returns:
            (None): This constructor does not return anything.

        Example:
            ```python
            headers = {"Authorization": "Bearer YOUR_TOKEN"}
            model_upload = ModelUpload(headers)
            ```

        Notes:
            This class inherits from `APIClient` and initiates connection settings specific to the model upload
            endpoint. Automatically configures agent name based on environment.
        """
        super().__init__(f"{HUB_API_ROOT}/v1/models", headers)
        self.name = "model"
        self.alive = True
        self.agent_id = None
        self.rate_limits = {"metrics": 3.0, "ckpt": 900.0, "heartbeat": 300.0}

    def upload_model(self, id, epoch, weights, is_best=False, map=0.0, final=False):
        """
        Uploads a model checkpoint to Ultralytics HUB.

        Args:
            id (int): Unique identifier for the model.
            epoch (int): The current training epoch.
            weights (str): Path to the model weights file.
            is_best (bool): Indicates if the current model is the best one so far.
            map (float): Mean average precision of the model.
            final (bool): Indicates if the model is the final model after training.

        Returns:
            (Response): HTTP response from the server.

        Example:
            ```python
            response = upload_model(id=123, epoch=10, weights='path/to/weights.pt', is_best=True, map=0.85, final=True)
            ```

        Notes:
            Ensure the weights file path is correctly specified and the file exists before calling this method.

        References:
            - [Ultralytics HUB Documentation](https://hub.ultralytics.com/)
            - [APIClient Documentation](https://requests.readthedocs.io/en/latest/api/#requests.Response)
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
        Performs uploading of metrics to the Ultralytics HUB for a specific model entity.

        Args:
            id (str): The unique identifier of the model entity to which the metrics are being uploaded.
            data (dict): The metrics data to upload, structured as a dictionary.

        Returns:
            (Optional[Response]): Response object from the `upload_metrics` request, or None if the request fails.

        Example:
            ```python
            model_upload = ModelUpload(headers={"Authorization": "Bearer your_api_key"})
            metrics_data = {"accuracy": 0.95, "loss": 0.05}
            response = model_upload.upload_metrics("model_id", metrics_data)
            ```

        References:
            [Ultralytics Hub API Documentation](https://hub.ultralytics.com/docs)
            [Requests Library](https://docs.python-requests.org/en/latest/)
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
        Export a file for a specific entity in a specified format.

        Args:
            id (str): The unique identifier of the entity to be exported.
            format (str): The format in which the file should be exported.

        Returns:
            (Optional[Response]): Response object from the export request, or None if it fails.

        References:
            [requests Response object](https://docs.python-requests.org/en/latest/api/#requests.Response)
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

        This method initiates a threaded loop that periodically sends heartbeats to the Ultralytics HUB to report
        the status of the agent. Heartbeats are sent at regular intervals as defined in the 'rate_limits' dictionary.

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

        This method stops the threaded loop responsible for sending heartbeats to the Ultralytics HUB by setting
        the 'alive' flag to False. This causes the loop in '_start_heartbeats' to exit.

        Returns:
            (None): The method does not return a value.
        """
        self.alive = False
        self.logger.debug("Heartbeats stopped.")

    def _register_signal_handlers(self) -> None:
        """
        Register signal handlers for SIGTERM and SIGINT signals to gracefully handle termination.

        This method sets up the handling of SIGTERM and SIGINT signals, allowing for a clean and controlled
        shutdown process by invoking the `_handle_signal` method when these signals are received.

        Returns:
            (None): The method does not return a value.

        References:
            [Python signal module](https://docs.python.org/3/library/signal.html)
        """
        signal.signal(signal.SIGTERM, self._handle_signal)  # Polite request to terminate
        signal.signal(signal.SIGINT, self._handle_signal)  # CTRL + C

    def _handle_signal(self, signum: int, frame: Any) -> None:
        """
        Handle kill signals and prevent heartbeats from being sent on Colab after termination.

        Args:
            signum (int): Signal number indicating the type of signal received.
            frame (Any): The current stack frame (not used in this method).

        Returns:
            (None): The method does not return a value.

        Notes:
            This method registers the signal to handle termination signals. The `frame` argument is included
            because it is passed by the signal handling mechanism but is not used in this method.
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
            config (Dict[str, Any]): Configuration parameters for the prediction.

        Returns:
            (Optional[Response]): Response object from the predict request, or None if upload fails.

        Example:
            ```python
            model = ModelUpload(headers={'Authorization': 'Bearer YOUR_TOKEN'})
            config = {"conf_threshold": 0.5}
            response = model.predict(id="12345", image="path/to/image.jpg", config=config)
            ```

        References:
            [requests.Response](https://docs.python-requests.org/en/latest/api/#requests.Response)
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
    Class for uploading project data to the Ultralytics HUB.

    This class provides methods for uploading project-related files to the Ultralytics HUB using the provided API
    headers during initialization.

    Attributes:
        name (str): Name identifier, set to "project".

    Methods:
        upload_image: Uploads an image file to a specified project on the Ultralytics HUB.

    Example:
        ```python
        headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
        project_upload = ProjectUpload(headers=headers)
        response = project_upload.upload_image(id="project_id", file="path/to/image.jpg")
        if response is not None and response.ok:
            print("Image uploaded successfully.")
        ```

    References:
        - [Ultralytics HUB API Documentation](https://docs.ultralytics.com)
    """

    def __init__(self, headers: dict):
        """
        Initialize the ProjectUpload class for managing project uploads in Ultralytics HUB.

        Args:
            headers (dict): Dictionary containing the headers to be used for API requests.

        Returns:
            (None): This method does not return a value.

        References:
            [Requests Documentation](https://docs.python-requests.org/en/master/)
        """
        super().__init__(f"{HUB_API_ROOT}/v1/projects", headers)
        self.name = "project"

    def upload_image(self, id: str, file: str) -> Optional[Response]:
        """
        Upload a project image file to Ultralytics HUB.

        Args:
            id (str): The unique identifier of the project to upload the image to.
            file (str): The local filesystem path to the image file to be uploaded.

        Returns:
            (Optional[Response]): Response object from the upload image request, or None if it fails.

        Notes:
            Ensure the specified image file exists at the given path before calling this function.

        Example:
            ```python
            project_upload = ProjectUpload(headers={"Authorization": "Bearer your_api_token"})
            response = project_upload.upload_image("project_id", "path/to/image.jpg")
            ```
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
    DatasetUpload class for uploading dataset files to Ultralytics HUB.

    This class provides functionality for uploading dataset files associated with specific IDs to the Ultralytics HUB.

    Attributes:
        name (str): Identifier for the type of entity being uploaded (in this case, "dataset").

    Methods:
        upload_dataset: Uploads a dataset file to the Ultralytics HUB.

    Example:
        ```python
        dataset_uploader = DatasetUpload(headers={'Authorization': 'Bearer YOUR_API_KEY'})
        response = dataset_uploader.upload_dataset('your-dataset-id', 'path/to/your/dataset.zip')
        if response:
            print("Dataset uploaded successfully.")
        else:
            print("Dataset upload failed.")
        ```

    References:
        [Ultralytics HUB SDK Documentation](https://github.com/ultralytics/hub-sdk)
    """

    def __init__(self, headers: dict):
        """
        Initializes the DatasetUpload class with the specified headers for API requests.

        Args:
            headers (dict): HTTP headers to include in the requests made by this client.

        Returns:
            (None): This method does not return a value.

        Example:
            ```python
            headers = {"Authorization": "Bearer YOUR_TOKEN"}
            dataset_uploader = DatasetUpload(headers)
            ```

        References:
            - [HTTP Headers in the requests library](https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers)
        """
        super().__init__(f"{HUB_API_ROOT}/v1/datasets", headers)
        self.name = "dataset"

    def upload_dataset(self, id, file) -> Optional[Response]:
        """
        Upload a dataset file to the Ultralytics HUB.

        Args:
            id (str): The ID of the dataset to upload.
            file (str): The path to the dataset file to upload.

        Returns:
            (Optional[Response]): Response object from the upload dataset request, or None if it fails.

        Example:
            ```python
            headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
            dataset_upload = DatasetUpload(headers)
            response = dataset_upload.upload_dataset("dataset_id", "/path/to/dataset.zip")
            ```
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
