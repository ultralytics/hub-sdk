from pathlib import Path
from .config import HUB_WEB_ROOT
from .logger import Logger
from .api_client import APIClientMixin


class ModelUpload(APIClientMixin):
    def __init__(self, headers):
        super().__init__(HUB_WEB_ROOT, "models", headers)
        self.name = "model"
        self.logger = Logger(self.name).get_logger()

    def upload_model(self, epoch, weights, is_best=False, map=0.0, final=False):
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
            if Path(weights).is_file():
                with open(weights, 'rb') as f:
                    file = f.read()
            else:
                self.logger.warning(f'WARNING ⚠️ Model upload issue. Missing model {weights}.')
                file = None

            endpoint = f"/{id}/upload"
            data = {'epoch': epoch}
            if final:
                data.update({'type': 'final', 'map': map})
                files = {'best.pt': file}
            else:
                data.update({'type': 'epoch', 'isBest': bool(is_best)})
                files = {'last.pt': file}
            
            return self._handle_request(self.api_client.post, endpoint, data, files=files)
        except Exception as e:
            self.logger.error(f"Failed to upload file for {self.name}: %s", e)

    def upload_metrics(self, id, data):
        """
        Upload a file for a specific entity.

        Args:
            id (str): The unique identifier of the entity to which the file is being uploaded.
            file (str): Path to the file to be uploaded.

        Returns:
            dict or None: Response data if successful, None on failure.
        """
        try:
            payload = {'metrics': data, 'type': 'metrics'}
            endpoint = f"/{id}"
            return self._handle_request(self.api_client.post, endpoint, payload)
        except Exception as e:
            self.logger.error(f"Failed to upload file for {self.name}: %s", e)
