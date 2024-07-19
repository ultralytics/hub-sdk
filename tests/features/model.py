import json
import time

import requests

from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class Model(BaseClass):
    """
    A Model class for managing and interacting with machine learning models.

    This class provides methods to create, update, retrieve, delete, export, and upload models, as well as manage metrics
    and checkpoints.

    Attributes:
        client (object): The client object used for interacting with models.

    Methods:
        get_model_by_id(model_id: str) -> Model:
            Retrieves a model by its ID.
        create_new_model(data: dict) -> str:
            Creates a new model with the provided data.
        is_model_exists(model_id: str) -> bool:
            Checks if a model with the specified ID exists.
        update_model(model_id: str, data: dict):
            Updates an existing model with the provided data.
        get_model_name(model_id: str) -> str:
            Retrieves the name of a model based on its ID.
        delete_model(model_id: str):
            Deletes a model based on its ID.
        list_public_models() -> list:
            Retrieves a list of public models.
        upload_model_metrics(model_id: str, data: dict):
            Uploads metrics data for a specific model.
        export_model(model_id: str, format_name: str):
            Exports a model in the specified format.
        is_model_exported(model_id: str, format_name: str) -> bool:
            Checks if a model has been successfully exported in the specified format.
        get_model_download_link(model_id: str) -> str:
            Retrieves the download link for a specific model.
        upload_model_checkpoint(model_id: str, model_checkpoint_file) -> requests.Response:
            Uploads a model checkpoint file for a specific model.
        is_checkpoint_uploaded(response: requests.Response) -> bool:
            Determines if a model checkpoint was successfully uploaded.
        is_metrics_updated(data: dict, metrics: list) -> bool:
            Check if the provided metrics match corresponding values in the data.
        get_model_metrics(model_id: str) -> dict:
            Retrieve metrics for the specified model.

    Example:
        ```python
        client = SomeClient()
        model_manager = Model(client)
        data = {'name': 'NewModel', 'type': 'Classification'}

        # Create a new model
        model_id = model_manager.create_new_model(data)

        # Check if the model exists
        exists = model_manager.is_model_exists(model_id)

        # Export the model
        model_manager.export_model(model_id, 'ONNX')

        # Retrieve model metrics
        metrics = model_manager.get_model_metrics(model_id)
        ```
    References:
        [Requests library](https://docs.python-requests.org/en/master/)
        [JSON library](https://docs.python.org/3/library/json.html)
    """

    def __init__(self, client):
        """
        Initializes a new instance of the Model class.

        Args:
            client (requests.Session): The client session object used for interacting with models.

        Returns:
            None

        Example:
            ```python
            client = requests.Session()
            model = Model(client)
            ```

        Notes:
            The client should be an active and properly authenticated instance of requests.Session.

        References:
            [requests.Session documentation](https://docs.python-requests.org/en/latest/api/#requests.Session)
        """
        self.client = client

    def get_model_by_id(self, model_id):
        """
        Retrieves a model by its ID.

        Args:
            model_id (str): The ID of the model to be retrieved.

        Returns:
            (Model): The model object associated with the provided ID.

        Example:
            ```python
            model = Model(client)
            my_model = model.get_model_by_id("12345")
            ```
        """
        self.delay()
        return self.client.model(model_id)

    def create_new_model(self, data):
        """
        Creates a new model with the provided data.

        Args:
            data (dict): A dictionary containing the details required for model creation.

        Returns:
            (str): The ID of the newly created model.

        Example:
            ```python
            data = {"name": "new_model", "description": "A new model for the project"}
            model_id = model.create_new_model(data)
            ```
        """
        self.delay()
        model = self.client.model()
        self.delay()
        model.create_model(data)
        return model.id

    def is_model_exists(self, model_id):
        """
        Checks if a model with the specified ID exists.

        Args:
            model_id (str): The ID of the model.

        Returns:
            (bool): True if the model exists, False otherwise.

        Example:
            ```python
            model_instance = Model(client)
            exists = model_instance.is_model_exists("12345abc")
            ```
        """
        try:
            model = self.get_model_by_id(model_id)
            model_data = model.data
            return bool(model_data)
        except Exception as e:
            log = self.get_logger()
            log.error(e)
            return False

    def update_model(self, model_id, data):
        """
        Updates an existing model with the provided data.

        Args:
            model_id (str): The ID of the model to update.
            data (dict): The data to update the model.

        References:
            [Requests Library](https://docs.python-requests.org/en/master/)
            [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

        Example:
            ```python
            client = SomeClientImplementation()
            model = Model(client)
            updated_data = {"name": "New Model Name", "parameters": {...}}
            model.update_model("model123", updated_data)
            ```
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        model.update(data)

    def get_model_name(self, model_id):
        """
        Retrieves the name of a model based on its ID.

        Args:
            model_id (str): The ID of the model.

        Returns:
            (str): The name of the model.

        Example:
            ```python
            model_instance = Model(client)
            model_name = model_instance.get_model_name("1234")
            ```
        """
        self.delay()
        return self.client.model(model_id).data["meta"]["name"]

    def delete_model(self, model_id):
        """
        Deletes a model based on its ID.

        Args:
            model_id (str): The ID of the model to delete.

        Returns:
            None

        Notes:
            Ensure that the model ID is valid and the model exists before invoking this method.

        Example:
            ```python
            model_instance = Model(client)
            model_instance.delete_model("12345")
            ```
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        model.delete(hard=True)

    def list_public_models(self):
        """
        Retrieves a list of public models.

        Returns:
            (list[dict]): A list of dictionaries representing public models, limited to a page size of 10.

        Notes:
            The function introduces a delay before making the API call to retrieve the models.

        References:
            [Requests Library](https://docs.python-requests.org/en/latest/)
            [JSON](https://docs.python.org/3/library/json.html)

        Example:
            ```python
            model_instance = Model(client)
            public_models = model_instance.list_public_models()
            ```
        """
        self.delay()
        model_list = self.client.model_list(page_size=10, public=True)
        return model_list.results

    def upload_model_metrics(self, model_id, data):
        """
        Uploads metrics data for a specific model.

        Args:
            model_id (str): The ID of the model.
            data (dict): The metrics data to upload.

        Returns:
            None

        Notes:
            Ensure that the metrics data follows the expected format required by the server to prevent
            upload errors.
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        model.upload_metrics(data)

    def export_model(self, model_id, format_name):
        """
        Exports a model in the specified format.

        Args:
            model_id (str): The ID of the model to export.
            format_name (str): The format in which to export the model.

        Example:
            ```python
            model = Model(client)
            model.export_model("123abc", "ONNX")
            ```

        Notes:
            Supported formats may include ['ONNX', 'TF', 'TorchScript']. Ensure to check the compatibility of the format
            with your downstream tasks.
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        model.export(format_name)

    @staticmethod
    def is_model_exported(model_id, format_name):
        """
        Checks if a model has been successfully exported in the specified format.

        Args:
            model_id (str): The ID of the model.
            format_name (str): The format in which the model was exported.

        Returns:
            (bool): True if the model has been successfully exported, False otherwise.

        Example:
            ```python
            is_exported = Model.is_model_exported("12345", "ONNX")
            ```

        References:
            - [requests documentation](https://docs.python-requests.org/en/master/)
            - [json documentation](https://docs.python.org/3/library/json.html)
        """
        host = TestData().get_api_data()["host"]
        url = f"{host}/get-export"

        payload = json.dumps({"modelId": model_id, "format": format_name})
        headers = {"x-api-key": TestData().get_auth_data()["valid_api_key"], "Content-Type": "application/json"}

        start_time = time.time()
        timeout = 60

        while time.time() - start_time < timeout:
            response = requests.post(url=url, headers=headers, data=payload)
            data = response.json()

            if data.get("message") == "Export ready!":
                return True

            time.sleep(10)

        return False

    def get_model_download_link(self, model_id):
        """
        Retrieves the download link for a specific model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            str: The download link for the model.

        Example:
            ```python
            model = Model(client)
            download_link = model.get_model_download_link('model123')
            print(download_link)
            ```

        References:
            [JSON Specification](https://www.json.org/json-en.html)
            [Requests: HTTP for Humans](https://docs.python-requests.org/en/master/)
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        return model.get_weights_url("best")

    def upload_model_checkpoint(self, model_id, model_checkpoint_file):
        """
        Uploads a model checkpoint file for a specific model.

        Args:
            model_id (str): The ID of the model.
            model_checkpoint_file (file-like object): The file containing the model checkpoint data.

        Returns:
            (requests.Response): The response object from the checkpoint upload request.

        Notes:
            Ensure that the `model_checkpoint_file` is a valid file-like object compatible with the upload API.

        Example:
            ```python
            with open('checkpoint.pth', 'rb') as f:
                response = model.upload_model_checkpoint('model_id', f)
            ```

        References:
            [requests.Response Documentation](https://docs.python-requests.org/en/master/api/#requests.Response)
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        return model.upload_model(is_best=True, epoch=10, weights=model_checkpoint_file)

    @staticmethod
    def is_checkpoint_uploaded(response):
        """
        Determines if a model checkpoint was successfully uploaded.

        Args:
            response (requests.Response): The HTTP response object received from the checkpoint upload request.

        Returns:
            bool: True if the checkpoint was successfully uploaded, False otherwise.

        References:
            [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
        """
        return response is not None and response.status_code == 200

    @staticmethod
    def is_metrics_updated(data, metrics):
        """
        Check if the provided metrics match corresponding values in the data.

        Args:
            data (dict): Dictionary with numeric keys and JSON-encoded metric strings.
            metrics (list): List of dictionaries with 'meta' containing 'name' and 'data' with numeric key values.

        Returns:
            (bool): True if all metrics match corresponding data values, False otherwise.
        """
        for i in data.keys():
            current_data = json.loads(data[i])
            for metric in metrics:
                metric_name = metric["meta"]["name"]
                if metric_name in current_data and current_data[metric_name] != metric["data"][str(i)]:
                    return False
        return True

    def get_model_metrics(self, model_id):
        """
        Retrieves metrics for the specified model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            (dict): Metrics associated with the specified model.

        Example:
            ```python
            model_id = "12345"
            metrics = model.get_model_metrics(model_id)
            ```
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        return model.get_metrics()
