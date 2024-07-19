# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from typing import Any, Dict, List, Optional

from requests import Response

from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import ModelUpload
from hub_sdk.config import HUB_API_ROOT


class Models(CRUDClient):
    """
    A class for managing the lifecycle of models, including CRUD operations and interactions with the Ultralytics HUB.

    Attributes:
        base_endpoint (str): The base endpoint URL for API requests, set to "models".
        hub_client (ModelUpload): Instance used for uploading models and metrics.
        id (str | None): Unique model identifier.
        data (dict): Dictionary for storing model metadata.
        metrics (list[dict] | None): List for holding model performance metrics after retrieval.

    Methods:
        get_data: Retrieve and store model metadata based on the model ID.
        create_model: Create a new model using provided model metadata.
        is_resumable: Determine if training can be resumed.
        has_best_weights: Check for the presence of best weights.
        is_pretrained: Verify if the model is pretrained.
        is_trained: Confirm if the model's training is complete.
        is_custom: Identify if the model is customized.
        get_architecture: Fetch the model's architecture name.
        get_dataset_url: Obtain the URL of the associated dataset.
        get_weights_url: Acquire the URL showing model weights.
        delete: Remove the model from the system.
        update: Update the model's metadata.
        get_metrics: Retrieve the model's training or evaluation metrics.
        upload_model: Upload model checkpoints to Ultralytics HUB.
        upload_metrics: Submit model performance metrics to Ultralytics HUB.
        start_heartbeat: Send periodic heartbeat signals to a server.
        stop_heartbeat: Cease sending heartbeat signals.
        export: Export model in various supported formats.
        predict: Run inference on an image using the model.

    Example:
        ```python
        models_client = Models(model_id='model123')
        models_client.get_data()
        print(models_client.data)
        ```

    References:
        [Ultralytics Export Formats](https://docs.ultralytics.com/modes/export/#export-formats)
    """

    def __init__(self, model_id: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a Models instance.

        Args:
            model_id (str, optional): The unique identifier of the model.
            headers (Dict[str, Any], optional): Headers to be included in API requests.

        Returns:
            None

        Example:
            ```python
            models_instance = Models(model_id="12345", headers={"Authorization": "Bearer token"})
            ```

        References:
            - [requests documentation](https://docs.python-requests.org/en/master/)
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
    def _reconstruct_data(data: dict) -> dict:
        """
        Wraps and reconstructs model data into a standard format supported by Ultralytics.

        Args:
            data (dict): Dictionary containing model data which may include keys like 'batch_size', 'epochs',
                'imgsz', 'patience', 'device', 'cache'.

        Returns:
            (dict): Reconstructed data format organized within a 'config' dictionary.

        Example:
            ```python
            original_data = {
                "batch_size": 32,
                "epochs": 50,
                "imgsz": 640,
                "patience": 7,
                "device": "cuda",
                "cache": True
            }
            reconstructed_data = Models._reconstruct_data(original_data)
            # reconstructed_data is now:
            # {
            #     "config": {
            #         "batchSize": 32,
            #         "epochs": 50,
            #         "imageSize": 640,
            #         "patience": 7,
            #         "device": "cuda",
            #         "cache": True
            #     }
            # }
            ```
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
        Retrieves data for the current model instance from the API and reconstructs its format.

        Returns:
            (None): The method does not return a value.

        Notes:
            If the model ID is invalid or the server does not respond, an error message is logged, and the operation
            is halted.

        References:
            [requests.Response.json](https://docs.python-requests.org/en/master/api/#requests.Response.json)
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

    def create_model(self, model_data: dict) -> None:
        """
        Creates a new model with the provided data and sets the model ID for the current instance.

        Args:
            model_data (dict): A dictionary containing the data for creating the model.

        Returns:
            (None): The method does not return a value.

        Notes:
            This method interacts with the Ultralytics hub to create a model and updates the current instance's ID
            upon success. Ensure 'model_data' follows the required structure for model creation.

        Example:
            ```python
            models_instance = Models()
            model_data = {
                "name": "new_model",
                "batch_size": 16,
                "epochs": 50,
                "imgsz": 640,
            }
            models_instance.create_model(model_data)
            ```

        References:
            - [Ultralytics hub documentation](https://docs.ultralytics.com/)
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
        """
        Check if the model training can be resumed.

        Returns:
            (bool): True if resumable, False otherwise.

        Notes:
            This method checks specific criteria or attributes in the model's data to determine if training
            can be resumed.

        Example:
            ```python
            models = Models(model_id="abc123")
            if models.is_resumable():
                print("Model training is resumable")
            else:
                print("Model training cannot be resumed")
            ```

        References:
            - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
        """
        return self.data.get("has_last_weights", False)

    def has_best_weights(self) -> bool:
        """
        Checks if the model has best weights saved.

        Returns:
            (bool): True if best weights are available, False otherwise.

        Example:
            ```python
            model = Models(model_id="example_id")
            if model.has_best_weights():
                print("Best weights are available.")
            ```

        Notes:
            Best weights refer to the model weights recorded after achieving the highest metric score during training.
        """
        return self.data.get("has_best_weights", False)

    def is_pretrained(self) -> bool:
        """
        Check if the model is pretrained.

        Returns:
            (bool): True if pretrained, False otherwise.

        Example:
            ```python
            model = Models(model_id="12345")
            is_model_pretrained = model.is_pretrained()
            print(is_model_pretrained)
            ```

        Notes:
            This function checks the 'is_pretrained' attribute in the model's data to determine
            if the model is pretrained.
        """
        return self.data.get("is_pretrained", False)

    def is_trained(self) -> bool:
        """
        Check if the model is trained.

        Returns:
            (bool): True if trained, False otherwise.

        Example:
            ```python
            model = Models(model_id='12345')
            trained_status = model.is_trained()
            print(trained_status)  # Output: True or False
            ```
        """
        return self.data.get("status") == "trained"

    def is_custom(self) -> bool:
        """
        Check if the model is custom.

        Returns:
            (bool): True if custom, False otherwise.

        Example:
            ```python
            model = Models(model_id="12345")
            is_custom_model = model.is_custom()
            ```
        """
        return self.data.get("is_custom", False)

    def get_architecture(self) -> Optional[str]:
        """
        Get the architecture name of the model.

        Returns:
            (Optional[str]): The architecture name followed by '.yaml' or None if not available.

        Notes:
            The architecture name is typically defined during the model creation phase and is essential for
            understanding the model structure.
        """
        return self.data.get("cfg")

    def get_dataset_url(self) -> Optional[str]:
        """
        Retrieve the dataset URL associated with the model.

        Returns:
            (Optional[str]): The URL of the dataset or None if not available.

        Example:
            ```python
            model = Models(model_id="12345")
            dataset_url = model.get_dataset_url()
            ```

        References:
            - [requests.Response](https://docs.python-requests.org/en/latest/api/#requests.Response)
        """
        return self.data.get("data")

    def get_weights_url(self, weight: str = "best") -> Optional[str]:
        """
        Performs non-maximum suppression (NMS) on prediction boxes.

        Args:
            weight (str, optional): Type of weights to retrieve. Options are "best" (default) or "last".

        Returns:
            (Optional[str]): The URL of the specified weights or None if not available.

        Example:
            ```python
            model = Models(model_id="1234")
            weights_url = model.get_weights_url(weight="last")
            ```

        Notes:
            The function currently supports "best" and "last" weights for retrieval.

        References:
            - [Non-maximum Suppression](https://ieeexplore.ieee.org/document/1572007): Paper explaining the NMS technique.
        """
        if weight == "last":
            return self.data.get("resume")

        return self.data.get("weights")

    def delete(self, hard: bool = False) -> Optional[Response]:
        """
        Deletes the model resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard (permanent) delete. Defaults to False.

        Note:
            The 'hard' parameter determines whether to perform a soft delete (default) or a hard delete.
            In a soft delete, the model might be marked as deleted but retained in the system.
            In a hard delete, the model is permanently removed from the system.

        Returns:
            (Optional[requests.Response]): Response object from the delete request, or None if delete fails.

        Example:
            ```python
            model_instance = Models(model_id="1234")
            response = model_instance.delete(hard=True)
            ```
        """
        return super().delete(self.id, hard)

    def update(self, data: dict) -> Optional[Response]:
        """
        Performs an update on an existing model resource represented by this instance.

        Args:
            data (dict): The updated data for the model resource.

        Returns:
            (Optional[Response]): Response object from the update request, or None if the update fails.

        Example:
            ```python
            model_data = {'name': 'new_model_name'}
            response = model.update(model_data)
            ```

        References:
            - [requests.Response](https://docs.python-requests.org/en/master/api/#requests.Response)
        """
        return super().update(self.id, data)

    def get_metrics(self) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve metrics for the model.

        Returns:
            (list[dict], optional): List of metrics objects or None if retrieval fails.

        Raises:
            Exception: If an error occurs during metrics retrieval.

        Example:
            ```python
            model = Models(model_id="12345")
            metrics = model.get_metrics()
            ```

        References:
            - [Ultralytics HUB API documentation](https://ultralytics.com/)
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
            is_best (bool): Indicates if the current model is the best one so far.
            map (float): Mean average precision of the model.
            final (bool): Indicates if the model is the final model after training.

        Returns:
            (Optional[Response]): Response object from the upload request, or None if upload fails.

        Example:
            ```python
            response = model.upload_model(epoch=10, weights='path/to/weights.pt', is_best=True, map=0.9, final=False)
            if response and response.status_code == 200:
                print("Upload successful!")
            ```
        """
        return self.hub_client.upload_model(self.id, epoch, weights, is_best=is_best, map=map, final=final)

    def upload_metrics(self, metrics: dict) -> Optional[Response]:
        """
        Uploads model metrics to Ultralytics HUB.

        Args:
            metrics (dict): A dictionary containing key-value pairs representing the model's performance metrics.

        Returns:
            (Optional[Response]): Response object from the upload metrics request, or None if the upload fails.

        Example:
            ```python
            metrics = {
                "accuracy": 0.95,
                "loss": 0.02,
            }
            response = model.upload_metrics(metrics)
            if response:
                print("Metrics uploaded successfully.")
            ```

        Notes:
            Ensure that the `metrics` dictionary follows the appropriate key-value structure expected by the
            Ultralytics HUB API.

        References:
            - [requests Response object](https://docs.python-requests.org/en/master/api/#requests.Response)
        """
        return self.hub_client.upload_metrics(self.id, metrics)  # response

    def start_heartbeat(self, interval: int = 60):
        """
        Starts sending heartbeat signals to a remote hub server.

        Args:
            interval (int): The time interval, in seconds, between consecutive heartbeats.

        Returns:
            (None): The method does not return a value.

        Note:
            Heartbeats are essential for maintaining a connection with the hub server and ensuring
            that the client remains active and responsive.
        """
        self.hub_client._register_signal_handlers()
        self.hub_client._start_heartbeats(self.id, interval)

    def stop_heartbeat(self) -> None:
        """
        Stops sending heartbeat signals to a remote hub server.

        This method terminates the transmission of heartbeat signals to the hub server, indicating that the client
        is no longer active or available.

        Returns:
            (None): The method does not return a value.

        Note:
            Stopping heartbeats should be performed with caution as the hub server may consider the client to be
            disconnected or inactive.
        """
        self.hub_client._stop_heartbeats()

    def export(self, format: str) -> Optional[Response]:
        """
        Export the model to Ultralytics HUB in the specified format.

        Args:
            format (str): The format to export the model in. Supports specific formats listed at
                [Ultralytics Export Formats](https://docs.ultralytics.com/modes/export/#export-formats).

        Returns:
            (Optional[Response]): Response object from the export request, or None if the export fails.

        Example:
            ```python
            model = Models("your_model_id")
            response = model.export(format="ONNX")
            if response:
                print("Export successful!")
            ```
        """
        return self.hub_client.export(self.id, format)  # response

    def predict(self, image: str, config: Dict[str, Any]) -> Optional[Response]:
        """
        Predict the object detections for an input image using the specified configuration.

        Args:
            image (str): The path to the image file to be processed for predictions.
            config (dict): A dictionary containing the configuration for the prediction in JSON format.

        Returns:
            (Optional[Response]): Response object from the predict request, or None if the prediction fails.

        Example:
            ```python
            model = Models(model_id="your_model_id")
            prediction_config = {"confidence_threshold": 0.4}
            result = model.predict("path/to/image.jpg", prediction_config)
            ```

        References:
            [Ultralytics Predict Configuration](https://docs.ultralytics.com/modes/predict/#configuration)
        """
        return self.hub_client.predict(self.id, image, config)  # response


class ModelList(PaginatedList):
    """
    A ModelList class for handling paginated lists of models from the Ultralytics platform.

    This class inherits from PaginatedList and provides functionalities for interacting with paginated data sets of models.

    Attributes:
        base_endpoint (str): The base API endpoint for model-related requests.
        page_size (Optional[int]): The number of models to fetch per page.
        public (Optional[bool]): Flag indicating whether to fetch public models.
        headers (Optional[Dict[str, Any]]): HTTP headers to include in requests.

    Methods:
        __init__: Initializes a ModelList instance.

    Example:
        ```python
        from ultralytics.models import ModelList

        model_list = ModelList(page_size=10, public=True, headers={'Authorization': 'Bearer token'})
        first_page = model_list.get_page(1)
        for model in first_page:
            print(model['id'], model['name'])
        ```

    References:
        [Ultralytics Documentation](https://docs.ultralytics.com/)
    """

    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a ModelList instance.

        Args:
            page_size (int | None): The number of items to request per page (default is None).
            public (bool | None): Whether the items should be publicly accessible (default is None).
            headers (dict | None): Headers to be included in API requests (default is None).

        Returns:
            (None): The method does not return a value.

        Notes:
            This class extends PaginatedList and is used to interact with a paginated list of models.

        References:
            - [Ultralytics Hub SDK](https://docs.ultralytics.com/)
        """
        base_endpoint = "models"
        super().__init__(base_endpoint, "model", page_size, public, headers)
