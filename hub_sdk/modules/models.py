# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from typing import Any, Dict, List, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import ModelUpload
from hub_sdk.config import HUB_API_ROOT


class Models(CRUDClient):
    """
    A class representing a client for interacting with Models through CRUD operations.

    This class extends the CRUDClient class and provides specific methods for working with Models, including
    creating, retrieving, updating, and deleting model resources, as well as uploading model weights and metrics.

    Attributes:
        base_endpoint (str): The base endpoint URL for the API, set to "models".
        hub_client (ModelUpload): An instance of ModelUpload used for interacting with model uploads.
        id (str | None): The unique identifier of the model, if available.
        data (Dict): A dictionary to store model data.
        metrics (List[Dict] | None): Model metrics data, populated after retrieval.

    Note:
        The 'id' attribute is set during initialization and can be used to uniquely identify a model.
        The 'data' attribute is used to store model data fetched from the API.
    """

    def __init__(self, model_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a Models instance.

        Args:
            model_id (str, optional): The unique identifier of the model.
            headers (Dict[str, Any], optional): Headers to be included in API requests.
        """
        self.base_endpoint = "models"
        super().__init__(self.base_endpoint, "model", headers)
        self.hub_client = ModelUpload(headers)
        self.id = model_id
        self.data = {}
        self.metrics = None
        if model_id:
            self.get_data()

    @staticmethod
    def _reconstruct_data(data: Dict) -> Dict:
        """
        Reconstruct format of model data supported by ultralytics.

        Args:
            data (Dict): Original model data dictionary.

        Returns:
            (Dict): Reconstructed data format with reorganized configuration.
        """
        if not data:
            return data

        data["config"] = {
            "batchSize": data.pop("batch_size", None),
            "epochs": data.pop("epochs", None),
            "imageSize": data.pop("imgsz", None),
            "patience": data.pop("patience", None),
            "device": data.pop("device", None),
            "cache": data.pop("cache", None),
        }

        return data

    def get_data(self) -> None:
        """
        Retrieve data for the current model instance.

        Fetches model data from the API if a valid model ID has been set and stores it in the instance. Logs appropriate
        error messages if the retrieval fails at any step.
        """
        if not self.id:
            self.logger.error("No model id has been set. Update the model id or create a model.")
            return

        try:
            response = super().read(self.id)

            if response is None:
                self.logger.error(f"Received no response from the server for model ID: {self.id}")
                return

            # Check if the response has a .json() method (it should if it's a response object)
            if not hasattr(response, "json"):
                self.logger.error(f"Invalid response object received for model ID: {self.id}")
                return

            resp_data = response.json()
            if resp_data is None:
                self.logger.error(f"No data received in the response for model ID: {self.id}")
                return

            data = resp_data.get("data", {})
            self.data = self._reconstruct_data(data)
            self.logger.debug(f"Model data retrieved for ID: {self.id}")

        except Exception as e:
            self.logger.error(f"An error occurred while retrieving data for model ID: {self.id}, {str(e)}")

    def create_model(self, model_data: Dict) -> None:
        """
        Create a new model with the provided data and set the model ID for the current instance.

        Args:
            model_data (Dict): A dictionary containing the data for creating the model.
        """
        try:
            response = super().create(model_data)

            if response is None:
                self.logger.error("Received no response from the server while creating the model.")
                return

            # Ensuring the response object has the .json() method
            if not hasattr(response, "json"):
                self.logger.error("Invalid response object received while creating the model.")
                return

            resp_data = response.json()
            if resp_data is None:
                self.logger.error("No data received in the response while creating the model.")
                return

            self.id = resp_data.get("data", {}).get("id")

            # Check if the ID was successfully retrieved
            if not self.id:
                self.logger.error("Model ID not found in the response data.")
                return

            self.get_data()

        except Exception as e:
            self.logger.error(f"An error occurred while creating the model: {str(e)}")

    def is_resumable(self) -> bool:
        """Check if the model training can be resumed based on the presence of last weights."""
        return self.data.get("has_last_weights", False)

    def has_best_weights(self) -> bool:
        """Check if the model has best weights saved from previous training."""
        return self.data.get("has_best_weights", False)

    def is_pretrained(self) -> bool:
        """Check if the model is pretrained with initial weights."""
        return self.data.get("is_pretrained", False)

    def is_trained(self) -> bool:
        """Check if the model has completed training and is in 'trained' status."""
        return self.data.get("status") == "trained"

    def is_custom(self) -> bool:
        """Check if the model is a custom model rather than a standard one."""
        return self.data.get("is_custom", False)

    def get_architecture(self) -> Optional[str]:
        """
        Get the architecture name of the model.

        Returns:
            (Optional[str]): The architecture configuration path or None if not available.
        """
        return self.data.get("cfg")

    def get_dataset_url(self) -> Optional[str]:
        """
        Get the dataset URL associated with the model.

        Returns:
            (Optional[str]): The URL of the dataset or None if not available.
        """
        return self.data.get("data")

    def get_weights_url(self, weight: str = "best") -> Optional[str]:
        """
        Get the URL of the model weights.

        Args:
            weight (str, optional): Type of weights to retrieve, either "best" or "last".

        Returns:
            (Optional[str]): The URL of the specified weights or None if not available.
        """
        if weight == "last":
            return self.data.get("resume")

        return self.data.get("weights")

    def delete(self, hard: bool = False) -> Optional[Response]:
        """
        Delete the model resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard (permanent) delete.

        Note:
            The 'hard' parameter determines whether to perform a soft delete (default) or a hard delete.
            In a soft delete, the model might be marked as deleted but retained in the system.
            In a hard delete, the model is permanently removed from the system.

        Returns:
            (Optional[Response]): Response object from the delete request, or None if delete fails.
        """
        return super().delete(self.id, hard)

    def update(self, data: Dict) -> Optional[Response]:
        """
        Update the model resource represented by this instance.

        Args:
            data (Dict): The updated data for the model resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if update fails.
        """
        return super().update(self.id, data)

    def get_metrics(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get metrics of the model.

        Returns:
            (Optional[List[Dict[str, Any]]]): The list of metrics objects, or None if retrieval fails.
        """
        if self.metrics:
            return self.metrics

        endpoint = f"{HUB_API_ROOT}/v1/{self.base_endpoint}/{self.id}/metrics"
        try:
            results = self.get(endpoint)
            self.metrics = results.json().get("data")
            return self.metrics
        except Exception as e:
            self.logger.error(f"Model Metrics not found: {e}")
            return None

    def upload_model(
        self,
        epoch: int,
        weights: str,
        is_best: bool = False,
        map: float = 0.0,
        final: bool = False,
    ) -> Optional[Response]:
        """
        Upload a model checkpoint to Ultralytics HUB.

        Args:
            epoch (int): The current training epoch.
            weights (str): Path to the model weights file.
            is_best (bool, optional): Indicates if the current model is the best one so far.
            map (float, optional): Mean average precision of the model.
            final (bool, optional): Indicates if the model is the final model after training.

        Returns:
            (Optional[Response]): Response object from the upload request, or None if upload fails.
        """
        return self.hub_client.upload_model(self.id, epoch, weights, is_best=is_best, map=map, final=final)

    def upload_metrics(self, metrics: Dict) -> Optional[Response]:
        """
        Upload model metrics to Ultralytics HUB.

        Args:
            metrics (Dict): Dictionary containing model metrics data.

        Returns:
            (Optional[Response]): Response object from the upload metrics request, or None if it fails.
        """
        return self.hub_client.upload_metrics(self.id, metrics)  # response

    def start_heartbeat(self, interval: int = 60):
        """
        Start sending heartbeat signals to a remote hub server.

        This method initiates the sending of heartbeat signals to a hub server
        to indicate the continued availability and health of the client.

        Args:
            interval (int, optional): The time interval, in seconds, between consecutive heartbeats.

        Note:
            Heartbeats are essential for maintaining a connection with the hub server
            and ensuring that the client remains active and responsive.
        """
        self.hub_client._register_signal_handlers()
        self.hub_client._start_heartbeats(self.id, interval)

    def stop_heartbeat(self) -> None:
        """
        Stop sending heartbeat signals to a remote hub server.

        This method terminates the sending of heartbeat signals to the hub server,
        effectively signaling that the client is no longer available or active.

        Note:
            Stopping heartbeats should be done carefully, as it may result in the hub server
            considering the client as disconnected or unavailable.
        """
        self.hub_client._stop_heartbeats()

    def export(self, format: str) -> Optional[Response]:
        """
        Export model to specified format via Ultralytics HUB.

        Args:
            format (str): Export format. Supported formats are available at
                https://docs.ultralytics.com/modes/export/#export-formats

        Returns:
            (Optional[Response]): Response object from the export request, or None if export fails.
        """
        return self.hub_client.export(self.id, format)  # response

    def predict(self, image: str, config: Dict[str, Any]) -> Optional[Response]:
        """
        Run prediction using the model via Ultralytics HUB.

        Args:
            image (str): The path to the image file.
            config (Dict[str, Any]): A configuration dictionary for the prediction.

        Returns:
            (Optional[Response]): Response object from the predict request, or None if prediction fails.
        """
        return self.hub_client.predict(self.id, image, config)  # response


class ModelList(PaginatedList):
    """Provides a paginated list interface for managing and querying models from the Ultralytics HUB API."""

    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a ModelList instance.

        Args:
            page_size (int, optional): The number of items to request per page.
            public (bool, optional): Whether the items should be publicly accessible.
            headers (Dict, optional): Headers to be included in API requests.
        """
        base_endpoint = "models"
        super().__init__(base_endpoint, "model", page_size, public, headers)
