import os
import platform
import sys
from time import sleep
from pathlib import Path
from .config import HUB_API_ROOT
from .api_client import APIClient
from .utils import threaded
import signal


def is_colab():
    return 'google.colab' in platform.sys.modules
__version__ = sys.version.split()[0]

AGENT_NAME = f'python-{__version__}-colab' if is_colab() else f'python-{__version__}-local'

class ModelUpload(APIClient):
    def __init__(self, headers):
        super().__init__(f"{HUB_API_ROOT}/v1/models", headers)
        self.name = "model"
        self.alive = True
        self.agent_id = None
        self.rate_limits = {'metrics': 3.0, 'ckpt': 900.0, 'heartbeat': 300.0}

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
            base_path = os.getcwd()
            if Path(f"{base_path}/{weights}").is_file():
                with open(weights, 'rb') as f:
                    file = f.read()

                    endpoint = f"/{id}/upload"
                    data = {'epoch': epoch}
                    if final:
                        data.update({'type': 'final', 'map': map})
                        files = {'best.pt': file}
                    else:
                        data.update({'type': 'epoch', 'isBest': bool(is_best)})
                        files = {'last.pt': file}
            r = self.post(endpoint, data=data, files=files)
            msg = "Model optimized weights uploaded." if final else "Model checkpoint weights uploaded."
            self.logger.debug(msg)
            return r
        except Exception as e:
            self.logger.error(f"Failed to upload file for {self.name}: %s", e)
            raise e

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
            endpoint = f"{HUB_API_ROOT}/v1/models/{id}"
            r = self.post(endpoint, json=payload)
            self.logger.debug(f'Model metrics uploaded.')
            return r
        except Exception as e:
            self.logger.error(f"Failed to upload file for {self.name}: %s", e)
            raise e

    @threaded
    def _start_heartbeats(self, model_id, interval):
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
        endpoint = f'{HUB_API_ROOT}/v1/agent/heartbeat/models/{model_id}'
        try:
            self.logger.debug(f'Heartbeats started at {interval}s interval.')
            while self.alive:
                payload = {
                    'agent': AGENT_NAME,
                    'agentId': self.agent_id,
                }
                res = self.post(endpoint, json=payload).json()
                new_agent_id = res.get("data",{}).get("agentId")

                self.logger.debug('Heartbeat sent.')

                # Update the agent id as requested by the server
                if new_agent_id != self.agent_id:
                    self.logger.debug('Agent Id updated.')
                    self.agent_id = new_agent_id
                sleep(interval)
        except Exception as e:
            self.logger.error(f"Failed to start heartbeats: {e}")
            raise e

    def _stop_heartbeats(self):
        """
        Stop the threaded heartbeat loop.

        This method stops the threaded loop responsible for sending heartbeats to the Ultralytics HUB.
        It sets the 'alive' flag to False, which will cause the loop in '_start_heartbeats' to exit.

        Returns:
            None

        """
        self.alive = False
        self.logger.debug('Heartbeats stopped.')

    def _register_signal_handlers(self):
        """Register signal handlers for SIGTERM and SIGINT signals to gracefully handle termination."""
        signal.signal(signal.SIGTERM, self._handle_signal) # Polite request to terminate
        signal.signal(signal.SIGINT, self._handle_signal) # CTRL + C

    def _handle_signal(self, signum, frame):
        """
        Handle kill signals and prevent heartbeats from being sent on Colab after termination.
        This method does not use frame, it is included as it is passed by signal.
        """
        self.logger.debug('Kill signal received!')
        self._stop_heartbeats()
        sys.exit(signum)
