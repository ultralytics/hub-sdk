import json
import time
import requests
from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class Model(BaseClass):
    def __init__(self, client):
        """
        Initializes a new instance of the ModelPage class.

        Args:
            client: The client object used for interacting with models.
        """
        self.client = client

    def get_model_by_id(self, model_id):
        """
        Retrieves a model by its ID.

        Args:
            model_id (str): The ID of the model.

        Returns:
            Model: The model object.
        """
        self.delay()
        return self.client.model(model_id)

    def create_new_model(self, data):
        """
        Creates a new model with the provided data.

        Args:
            data (dict): The data to create the model.

        Returns:
            str: The ID of the newly created model.
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
            bool: True if the model exists, False otherwise.
        """
        try:
            model = self.get_model_by_id(model_id)
            model_data = model.data
            if not model_data:
                return False
            else:
                return True
        except Exception as e:
            log = self.getLogger()
            log.error(e)
            return False

    def update_model(self, model_id, data):
        """
        Updates an existing model with the provided data.

        Args:
            model_id (str): The ID of the model to update.
            data (dict): The data to update the model.
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
            str: The name of the model.
        """
        self.delay()
        return self.client.model(model_id).data["meta"]["name"]

    def delete_model(self, model_id):
        """
        Deletes a model based on its ID.

        Args:
            model_id (str): The ID of the model to delete.
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        model.delete(hard=True)

    def list_public_models(self):
        """
        Retrieves a list of public models.

        Returns:
            list: A list of public models, limited to a page size of 10.
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
            bool: True if the model has been successfully exported, False otherwise.
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
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        return model.get_weights_url("best")

    def upload_model_checkpoint(self, model_id, model_checkpoint_file):
        """
        Uploads a model checkpoint file for a specific model.

        Args:
            model_id (str): The ID of the model.
            model_checkpoint_file: The file containing the model checkpoint data.

        Returns:
            Response: The response object from the checkpoint upload request
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        response = model.upload_model(is_best=True, epoch=10, weights=model_checkpoint_file)
        return response

    @staticmethod
    def is_checkpoint_uploaded(response):
        """
        Determines if a model checkpoint was successfully uploaded.

        Args:
            response: The response object received from the checkpoint upload request.

        Returns:
            bool: True if the checkpoint was successfully uploaded, False otherwise.
        """
        if response is None:
            return False
        else:
            if response.status_code == 200:
                return True
            else:
                return False

    @staticmethod
    def is_metrics_updated(data, metrics):
        """
        Check if the provided metrics match corresponding values in the data.

        Parameters:
        - data (dict): Dictionary with numeric keys and JSON-encoded metric strings.
        - metrics (list): List of dictionaries with 'meta' containing 'name' and 'data' with numeric key values.

        Returns:
        - bool: True if all metrics match corresponding data values, False otherwise.
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
        Retrieve metrics for the specified model.

        Parameters:
        - model_id (str):  The ID of the model.

        Returns:
        - dict: Metrics associated with the specified model.
        """
        model = self.get_model_by_id(model_id)
        self.delay()
        return model.get_metrics()
