import platform
import sys
from time import sleep
from pathlib import Path
from .config import HUB_WEB_ROOT
from .logger import Logger
from .api_client import APIClientMixin
from .utils import threaded


def is_colab():
    return 'google.colab' in platform.sys.modules
__version__ = sys.version.split()[0]

AGENT_NAME = f'python-{__version__}-colab' if is_colab() else f'python-{__version__}-local'

class ModelUpload(APIClientMixin):
    def __init__(self, headers):
        super().__init__(HUB_WEB_ROOT, "models", headers)
        self.name = "model"
        self.alive = True
        self.agent_id = None
        self.rate_limits = {'metrics': 3.0, 'ckpt': 900.0, 'heartbeat': 300.0}
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

    @threaded
    def _start_heartbeats(self, model_id):
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
        endpoint = f'{HUB_WEB_ROOT}/v1/agent/heartbeat/models/{model_id}'
        payload = {
            'agent': AGENT_NAME,
            'agentID': self.agent_id,
        }
        try:
            while self.alive:
                res = self._handle_request(self.api_client.post, endpoint, payload)
                print("res",res)
                if res is None:
                    return None
                self.agent_id = res.get("agentID")
                sleep(self.rate_limits['heartbeat'])
        except Exception as e:
            self.logger.error(f"Failed to start heartbeats: {e}")

    def _stop_heartbeats(self):
        """
        Stop the threaded heartbeat loop.

        This method stops the threaded loop responsible for sending heartbeats to the Ultralytics HUB.
        It sets the 'alive' flag to False, which will cause the loop in '_start_heartbeats' to exit.

        Returns:
            None

        """
        self.alive = False
