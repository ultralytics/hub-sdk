from .server_clients import ModelUpload
from .crud_client import CRUDClient
from .paginated_list import PaginatedList
from .config import HUB_API_ROOT


class Models(CRUDClient):
    def __init__(self, arg, headers=None):
        """
        Initialize a Models instance.

        Args:
            headers (dict, optional): Headers to be included in API requests. Defaults to None.
        """
        super().__init__("models", "model", headers)
        self.hub_client = ModelUpload(headers)
        self.id = None 
        self.data =  {}

        if isinstance(arg, str):
            self.id = arg
            resp = super().read(arg)
        elif isinstance(arg, dict):
            resp = super().create(arg)

        self.data = resp.get("data",{}) if resp else {}
        self.id = self.data.get('id')

    def delete(self, hard=False):
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

    def update(self, data):
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

    def cleanup(self, id):
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
            return self._handle_request(self.api_client.delete, f"/{id}")
        except Exception as e:
            self.logger.error('Failed to cleanup: %s', e)

    def upload_model(self, epoch: int, weights: str, is_best: bool = False, map: float = 0.0, final: bool = False):
        """
        Upload a model checkpoint to Ultralytics HUB.

        Args:
            epoch (int): The current training epoch.
            weights (str): Path to the model weights file.
            is_best (bool): Indicates if the current model is the best one so far.
            map (float): Mean average precision of the model.
            final (bool): Indicates if the model is the final model after training.
        """
        return self.hub_client.upload_model(self.id, epoch, weights, is_best=is_best, map=map, final=final)
    
    def upload_metrics(self, metrics):
        """
        Upload model metrics to Ultralytics HUB.

        Args:
            metrics (dict):
        """
        resp = self.hub_client.upload_metrics(self.id, metrics)
        return resp

    def start_heartbeat(self):
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
        return self.hub_client._start_heartbeats(self.id)

    def stop_heartbeat(self):
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
        return self.hub_client._stop_heartbeats()

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
