import pytest

from tests.features.object_manager import ObjectManager
from tests.test_data.data import TestData
from tests.utils.base_class import BaseClass


class TestModel(BaseClass):
    """
    TestModel class for conducting various model-related tests in a machine learning environment.

    This class includes multiple test cases to verify functionalities like retrieving, creating, updating, deleting,
    listing, and exporting machine learning models.

    Methods:
        test_model_001: Verify successful retrieval of a model by ID.
        test_model_002: Verify project and dataset check functionality.
        test_model_003: Verify successful creation of a new model.
        test_model_004: Verify successful update of model metadata.
        test_model_005: Verify successful deletion of a model.
        test_model_006: Verify successful listing of public models.
        test_model_007: Verify successful upload of training metrics.
        test_model_008: Verify successful export of a model.
        test_model_009: Verify successful retrieval of model storage URL.
        test_model_010: Verify successful upload of a model checkpoint.

    References:
        [PyTest Documentation](https://docs.pytest.org/en/latest/)
    """

    @pytest.mark.smoke
    def test_model_001(self):
        """
        Verify successful retrieval of a model by ID.

        Args:
            None

        Returns:
            None

        Example:
            ```python
            test_instance = TestModel()
            test_instance.test_model_001()
            ```

        Notes:
            This function is decorated with pytest's @pytest.mark.smoke, indicating it is a smoke test.

        References:
            - [pytest.mark.smoke](https://docs.pytest.org/en/stable/mark.html#pytest-mark)
        """

        model_id = TestData().get_models_data()["valid_model_ID"]
        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()

        log = self.get_logger()
        log.info(f"Attempting to retrieve model with ID: {model_id}")

        model = model_obj.get_model_by_id(model_id)

        log.info(f"Model retrieved successfully. Model data: {model.data}")

        assert "config" in model.data, "Config information not found in the model data"
        assert "dataset" in model.data, "Dataset information not found in the model data"
        assert "project" in model.data, "Project information not found in the model data"

    @pytest.mark.smoke
    def test_model_002(self):
        """
        Verifies the retrieval and validity of specific project and dataset entities.

        Args:
            None

        Returns:
            None

        Example:
            ```python
            test_instance = TestModel()
            test_instance.test_model_002()
            ```

        Notes:
            This test checks that valid project and dataset IDs can be successfully retrieved and validated.

        References:
            [Pytest Documentation](https://docs.pytest.org/)
        """

        dataset_ID = TestData().get_datasets_data()["valid_dataset_ID"]
        project_ID = TestData().get_projects_data()["valid_project_ID"]
        object_manager = ObjectManager(self.client)

        log = self.get_logger()
        log.info(f"Attempting to retrieve project with ID: {project_ID}")

        project_obj = object_manager.get_project()
        project = project_obj.get_project_by_id(project_ID)

        log.info(f"Project retrieved successfully. Project ID: {project.id}")

        log.info(f"Attempting to retrieve dataset with ID: {dataset_ID}")

        dataset_obj = object_manager.get_dataset()
        dataset = dataset_obj.get_dataset_by_id(dataset_ID)

        log.info(f"Dataset retrieved successfully. Dataset ID: {dataset.id}")

        if None in (project.id, dataset.id):
            log.error("Project or Dataset ID is None. Assertion failed.")
            assert False
        else:
            log.info("Project and Dataset ID are not None. Assertion passed.")

    @pytest.mark.smoke
    def test_model_003(self, request, delete_test_model):
        """
        Verify successful creation of a new model.

        Args:
            request (pytest.FixtureRequest): The pytest request fixture providing information about the executing test.
            delete_test_model (pytest.FixtureFunction): The fixture function for removing test models after test execution.

        Returns:
            (None): This function does not return any value.

        Example:
            ```python
            def test_model():
                test_instance = TestModel()
                test_instance.test_model_003(request_fixture, delete_test_model_fixture)
            ```

        Notes:
            This test relies on previously defined pytest fixtures and assumes proper initialization of the client
            and logging within the TestModel class.
        """

        new_model_data = TestData().get_models_data()["new_model_data"]

        log = self.get_logger()

        log.info(f"Attempting to create a new model with the following data: {new_model_data}")

        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()

        # Create new model
        model_id = model_obj.create_new_model(new_model_data)

        log.info(f"New model created successfully. Model ID: {model_id}")

        # Set the model_id in the cache with a key that includes the test name
        test_name = request.node.name
        model_id_key = f"model_id_for_test_{test_name}"
        request.config.cache.set(model_id_key, model_id)

        assert model_obj.is_model_exists(model_id), f"Model with ID {model_id} does not exist."

    @pytest.mark.smoke
    def test_model_004(self, request, create_test_model, delete_test_model):
        """
        Verify successful update of model metadata.

        Args:
            request (pytest.FixtureRequest): Pytest fixture request object, used for test configuration and caching.
            create_test_model (function): Fixture function to create a test model for the test case.
            delete_test_model (function): Fixture function to delete the test model after the test case.

        Returns:
            (None): Does not return anything. Assertions within the test validate the success of the metadata update.

        Example:
            ```python
            def test_model_004(self, request, create_test_model, delete_test_model):
                # This pytest will setup and validate an update to a model's metadata
                self.test_model_004(request, create_test_model, delete_test_model)
            ```
        """

        # Retrieve necessary data
        test_name = request.node.name
        model_id_key = f"model_id_for_{test_name}"
        model_id = request.config.cache.get(model_id_key, None)
        desired_model_data = TestData().get_models_data()["desired_model_data"]
        desired_model_name = desired_model_data["meta"]["name"]

        log = self.get_logger()

        log.info(
            f"Attempting to update metadata for model with ID {model_id}. Desired model data: {desired_model_data}"
        )

        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()

        # Update model metadata
        model_obj.update_model(model_id, desired_model_data)

        log.info("Model metadata updated successfully.")

        # Get the updated model name
        updated_model_name = model_obj.get_model_name(model_id)

        log.info(f"Updated model name: {updated_model_name}")

        assert updated_model_name == desired_model_name, (
            f"Model name is not updated as expected. Actual:" f" {updated_model_name}, Expected: {desired_model_name}"
        )

    @pytest.mark.smoke
    def test_model_005(self, request, create_test_model):
        """
        Verify successful deletion of a model.

        Args:
            request (pytest.FixtureRequest): The fixture request object providing test manageability.
            create_test_model (function): Fixture to create a test model.

        Returns:
            None

        Notes:
            The model ID is retrieved from the pytest cache, which is set during the creation of the test model.

        Example:
            ```python
            def test_model_005(self, request, create_test_model):
                # This test assumes that a model has been created and its ID stored in the pytest cache
                self.test_model_005(request, create_test_model)
            ```
        """

        # Retrieve necessary data
        test_name = request.node.name
        model_id_key = f"model_id_for_{test_name}"
        model_id = request.config.cache.get(model_id_key, None)

        log = self.get_logger()

        log.info(f"Attempting to delete model with ID: {model_id}")

        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()

        # Delete the model
        model_obj.delete_model(model_id)

        log.info("Model deleted successfully.")

        # Assert that the model does not exist after deletion
        assert not model_obj.is_model_exists(model_id), f"Model with ID {model_id} still exists after deletion."

    @pytest.mark.smoke
    def test_model_006(self):
        """
        Verify successful listing of public models.

        Returns:
            (list[dict]): List of public models containing metadata, where each model is represented as a
                dictionary with keys such as 'dataset'.

        Example:
            ```python
            test_instance = TestModel()
            test_instance.test_model_006()
            ```

        Notes:
            This function uses the `ObjectManager` to retrieve a list of public models from the backend and logs
            detailed information about the process at various stages.

        References:
            - [pytest documentation](https://docs.pytest.org/en/latest/)
        """

        log = self.get_logger()

        log.info("Attempting to list public models.")

        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()

        # List public models
        public_model_list = model_obj.list_public_models()

        log.info(f"Public models listed successfully. Number of models: {len(public_model_list)}")

        assert "dataset" in public_model_list[0], "Dataset information not found in the model"
        assert "project" in public_model_list[0], "Project information not found in the model"

    @pytest.mark.smoke
    def test_model_007(self, request, create_test_model, delete_test_model):
        """
        Verify successful upload of training metrics.

        Args:
            request (pytest.FixtureRequest): The fixture request object, used to access test request context and config.
            create_test_model (fixture): Fixture to create a test model.
            delete_test_model (fixture): Fixture to delete the test model after testing.

        Returns:
            None

        Example:
            ```python
            def test_model_007(self, request, create_test_model, delete_test_model):
                # Function body here
            ```
        """

        log = self.get_logger()

        # Retrieve necessary data
        test_name = request.node.name
        model_id_key = f"model_id_for_{test_name}"
        model_id = request.config.cache.get(model_id_key, None)
        model_metrics_data = TestData().get_models_data()["desired_model_metrics"]

        # Initialize model objects
        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()

        # Upload model metrics
        log.info(f"Uploading metrics data for model ID: {model_id}")
        model_obj.upload_model_metrics(model_id, model_metrics_data)

        # Retrieve and verify updated metrics
        log.info(f"Retrieving updated metrics for model ID: {model_id}")
        updated_model_metrics = model_obj.get_model_metrics(model_id)

        log.info("Verifying if metrics are updated successfully")
        assert model_obj.is_metrics_updated(model_metrics_data, updated_model_metrics)
        log.info("Metrics verification passed successfully.")

    @pytest.mark.smoke
    def test_model_008(self, clear_export_model):
        """
        Verify successful export of a model.

        Args:
            clear_export_model (fixture): A pytest fixture to clear any exported model data before running the test.

        Returns:
            None

        Example:
            ```python
            def test_model_export(clear_export_model):
                test_model = TestModel()
                test_model.test_model_008(clear_export_model)
            ```

        Notes:
            - Ensure that the `clear_export_model` fixture is properly defined in your test suite to avoid unwanted side
              effects from previously exported models.

        References:
            [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
        """

        log = self.get_logger()

        # Retrieve necessary data
        model_id = TestData().get_models_data()["valid_model_ID"]
        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()
        desired_format = TestData().get_models_data()["desired_model_format"]

        # Export the model
        log.info(f"Exporting model {model_id} in {desired_format} format")
        model_obj.export_model(model_id, format_name=desired_format)

        # Check if the model is successfully exported
        export_status = model_obj.is_model_exported(model_id, format_name=desired_format)
        log.info(f"Model export status: {'Success' if export_status else 'Failure'}")

        assert export_status

    @pytest.mark.smoke
    def test_model_009(self):
        """
        Verify successful retrieval of model storage URL.

        Args:
            None

        Returns:
            (str): Model storage URL for downloading the specified model.

        Example:
            ```python
            test_model_instance = TestModel()
            storage_url = test_model_instance.test_model_009()
            ```
        """

        log = self.get_logger()

        model_id = TestData().get_models_data()["valid_model_ID"]

        log.info(f"Attempting to retrieve the storage URL for model with ID: {model_id}")

        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()

        # Get the model storage URL
        link = model_obj.get_model_download_link(model_id)

        log.info(f"Storage URL retrieved successfully. URL: {link}")

        assert f"{model_id}/best.pt" in link, f"Model ID not found in the storage URL: {link}"

    @pytest.mark.smoke
    def test_model_010(self, request, create_test_model, delete_test_model):
        """
        Verify successful upload of a model checkpoint.

        Args:
            request (pytest.FixtureRequest): The pytest request object to access test contextual data.
            create_test_model (pytest.Fixture): Fixture to handle test model creation.
            delete_test_model (pytest.Fixture): Fixture to handle test model deletion.

        Returns:
            None

        Example:
            ```python
            def test_model_010(self, request, create_test_model, delete_test_model):
                response = self.test_model_010(request, create_test_model, delete_test_model)
            ```
        """

        # Retrieve necessary data
        test_name = request.node.name
        model_id_key = f"model_id_for_{test_name}"
        model_id = request.config.cache.get(model_id_key, None)
        model_checkpoint_file = TestData().get_models_data()["model_checkpoint_file"]

        log = self.get_logger()

        log.info(f"Attempting to upload checkpoint for model with ID: {model_id}")

        object_manager = ObjectManager(self.client)
        model_obj = object_manager.get_model()

        # Upload model checkpoint
        response = model_obj.upload_model_checkpoint(model_id, model_checkpoint_file)

        log.info("Verifying if checkpoint uploaded successfully")
        assert model_obj.is_checkpoint_uploaded(response), "Model Checkpoint is not uploaded"
        log.info("Model checkpoint uploaded successfully.")
