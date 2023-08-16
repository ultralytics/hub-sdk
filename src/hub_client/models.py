from crud_client import CRUDClient


class Models(CRUDClient):
    def __init__(self):
        super().__init__("models", "model")


    def cleanup(self, id):
        try:
            return self._handle_request(self.api_client.delete, f"/{id}")
        except Exception as e:
            self.logger.error('Failed to cleanup: %s', e)