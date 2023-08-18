from .crud_client import CRUDClient


class Datasets(CRUDClient):
    def __init__(self, headers=None):
        super().__init__("datasets", "dataset", headers)


    def cleanup(self, id):
        try:
            return self._handle_request(self.api_client.delete, f"/{id}")
        except Exception as e:
            self.logger.error('Failed to cleanup: %s', e)
