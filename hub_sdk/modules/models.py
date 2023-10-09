# Quick hack for testing
import requests

from hub_sdk.config import HUB_FUNCTIONS_ROOT
from hub_sdk.base.crud_client import CRUDClient
from hub_sdk.base.paginated_list import PaginatedList
from hub_sdk.base.server_clients import ModelUpload


class Models(CRUDClient):
    def __init__(self, model_id=None, headers=None):
        """
        Initialize a Models instance.

        Args:
            headers (dict, optional): Headers to be included in API requests. Defaults to None.
        """
        super().__init__("models", "model", headers)
        self.hub_client = ModelUpload(headers)
        self.id = model_id
        self.data = {}

        if model_id:
            self.get_data()

    def get_data(self) -> None:
        """
        Retrieves data for the current model instance.

        If a valid model ID has been set, it sends a request to fetch the model data and stores it in the instance.
        If no model ID has been set, it logs an error message.

        Args:
            None

        Returns:
            None
        """
        if (self.id):
            resp = super().read(self.id).json()
            self.data = resp.get("data", {})
            self.logger.debug('Model id is %s', self.id)
        else:
            self.logger.error('No model id has been set. Update the model id or create a model.')

    def create_model(self, model_data: dict) -> None:
        """
        Creates a new model with the provided data and sets the model ID for the current instance.

        Args:
            model_data (dict): A dictionary containing the data for creating the model.

        Returns:
            None
        """
        resp = super().create(model_data).json()
        self.id = resp.get("data", {}).get('id')
        self.get_data()

    def is_resumable(self) -> bool:
        """
        Check if the model training can be resumed.

        Returns:
            bool: True if resumable, False otherwise.
        """
        return self.data.get('hasLastWeights', False)

    def has_best_weights(self) -> bool:
        """
        Check if the model has best weights saved.

        Returns:
            bool: True if best weights available, False otherwise.
        """
        return self.data.get('hasBestWeights', False)

    def is_pretrained(self) -> bool:
        """
        Check if the model is pretrained.

        Returns:
            bool: True if pretrained, False otherwise.
        """
        return self.data.get('isPretrained', False)

    def is_trained(self) -> bool:
        """
        Check if the model is trained.

        Returns:
            bool: True if trained, False otherwise.
        """
        return self.data.get('isTrained', False)

    def is_custom(self) -> bool:
        """
        Check if the model is custom.

        Returns:
            bool: True if custom, False otherwise.
        """
        return self.data.get('isCustom', False)

    def get_architecture(self) -> str:
        """
        Get the architecture name of the model.

        Returns:
            str or None: The architecture name followed by '.yaml' or None if not available.
        """
        name = self.data.get('lineage', {}).get('architecture', {}).get('name')
        return f"{name}.yaml" if name else None

    def get_dataset_url(self) -> str:
        """
        Get the dataset URL associated with the model.

        Returns:
            str or None: The URL of the dataset or None if not available.
        """
        resp = requests.post(
            f"{HUB_FUNCTIONS_ROOT}/v1/storage",
            json={"collection": "models", "docId": self.id, "object": "dataset"},
            headers=self.headers,
        )
        return resp.json().get("data", {}).get("url")

    def get_weights_url(self, weight: str = "best"):
        """
        Get the URL of the model weights.

        Args:
            weight (str, optional): Type of weights to retrieve. Defaults to "best".

        Returns:
            str or None: The URL of the specified weights or None if not available.
        """
        if weight != 'parent' or self.is_custom():
            resp = requests.post(
                f"{HUB_FUNCTIONS_ROOT}/v1/storage",
                json={"collection": "models", "docId": self.id, "object": weight},
                headers=self.headers,
            )
            return resp.json().get("data", {}).get("url")
        else:
            return self.data.get("lineage", {}).get("parent", {}).get("url")

    def delete(self, hard: bool =False) -> dict:
        """
        Delete the model resource represented by this instance.

        Args:
            hard (bool, optional): If True, perform a hard (permanent) delete. Defaults to False.

        Returns:
            dict: A dictionary containing the API response data after the deletion.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        return super().delete(self.id, hard)

    def update(self, data: dict) -> dict:
        """
        Update the model resource represented by this instance.

        Args:
            data (dict): The updated data for the model resource.

        Returns:
            dict: A dictionary containing the API response data after the update.

        Raises:
            Exception: If an error occurs during the update process.
        """
        return super().update(self.id, data)

    def cleanup(self, id: int) -> dict:
        """
        Delete a model resource by its ID.

        This method sends a DELETE request to the API to delete the model resource with the specified ID.

        Args:
            id (int): The ID of the model resource to be deleted.

        Returns:
            dict: A dictionary containing the API response data after the deletion.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            return self.delete(f"/{id}")
        except Exception as e:
            self.logger.error('Failed to cleanup: %s', e)

    def upload_model(
        self,
        epoch: int,
        weights: str,
        is_best: bool = False,
        map: float = 0.0,
        final: bool = False,
    ):
        """
        Upload a model checkpoint to Ultralytics HUB.

        Args:
            epoch (int): The current training epoch.
            weights (str): Path to the model weights file.
            is_best (bool): Indicates if the current model is the best one so far.
            map (float): Mean average precision of the model.
            final (bool): Indicates if the model is the final model after training.
        """
        return self.hub_client.upload_model(
            self.id, epoch, weights, is_best=is_best, map=map, final=final
        )

    def upload_metrics(self, metrics: dict):
        """
        Upload model metrics to Ultralytics HUB.

        Args:
            metrics (dict):
        """
        resp = self.hub_client.upload_metrics(self.id, metrics)
        return resp
    
    def get_download_link(self, type: str) -> str:
        """
        get model download link.

        Args:
            type (str):
        """
        try:
            payload = {'collection': "models", "docId" : self.id ,'object': type}
            endpoint =  f"{HUB_FUNCTIONS_ROOT}/v1/storage"
            response = self.post(endpoint, json=payload)
            json = response.json()
            return json.get("data",{}).get("url")
        except Exception as e:
            self.logger.error(f"Failed to download link for {self.name}: %s", e)
            raise e

    def start_heartbeat(self, interval: int =60):
        """
        Starts sending heartbeat signals to a remote hub server.

        This method initiates the sending of heartbeat signals to a hub server
        in order to indicate the continued availability and health of the client.

        Returns:
            bool: True if the heartbeat was successfully started, False otherwise.

        Note:
            Heartbeats are essential for maintaining a connection with the hub server
            and ensuring that the client remains active and responsive.
        """
        self.hub_client._register_signal_handlers()
        self.hub_client._start_heartbeats(self.id, interval)

    def stop_heartbeat(self) -> None:
        """
        Stops sending heartbeat signals to a remote hub server.

        This method terminates the sending of heartbeat signals to the hub server,
        effectively signaling that the client is no longer available or active.

        Returns:
            bool: True if the heartbeat was successfully stopped, False otherwise.

        Note:
            Stopping heartbeats should be done carefully, as it may result in the hub server
            considering the client as disconnected or unavailable.
        """
        self.hub_client._stop_heartbeats()

    def export(self, format):
        """
        export to Ultralytics HUB.

        Args: 
            export (dict):
        """
        resp = self.hub_client.export(self.id, format)
        return resp


class ModelList(PaginatedList):
    def __init__(self, page_size=None, public=None, headers=None):
        """
        Initialize a ModelList instance.

        Args:
            page_size (int, optional): The number of items to request per page. Defaults to None.
            public (bool, optional): Whether the items should be publicly accessible. Defaults to None.
            headers (dict, optional): Headers to be included in API requests. Defaults to None.
        """
        base_endpoint = "models"
        if public:
            base_endpoint = f"public/{base_endpoint}"
        super().__init__(base_endpoint, "model", page_size, headers)
