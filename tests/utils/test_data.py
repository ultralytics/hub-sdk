import base64
import json
import os
import sys

import firebase_admin
from firebase_admin import credentials, storage
from tqdm import tqdm


class FirebaseStorageManager:
    """
    A FirebaseStorageManager class for managing file operations in Firebase Storage.

    This class facilitates the initialization of Firebase Storage using provided credentials and the uploading
    and downloading of files between local directories and Firebase Storage.

    Attributes:
        firebase_cred (str): Path to the Firebase credentials JSON file.
        bucket_name (str): Name of the Firebase Storage bucket.
        bucket (firebase_admin.storage.bucket.Bucket): Storage bucket instance initialized based on given credentials.

    Methods:
        upload_test_data(local_folder, bucket_folder): Uploads files from the local directory to a specified folder in Firebase Storage.
        download_test_data(bucket_folder, local_folder): Downloads files from a specified folder in Firebase Storage to a local directory.

    Example:
        ```python
        firebase_manager = FirebaseStorageManager(firebase_cred='path/to/credentials.json', bucket_name='my_bucket')
        firebase_manager.upload_test_data(local_folder='/path/to/local/data', bucket_folder='firebase/data')
        firebase_manager.download_test_data(bucket_folder='firebase/data', local_folder='/path/to/local/data')
        ```

    Notes:
        - Ensure that the Firebase credentials file is correctly formatted and has sufficient permissions.

    References:
        - [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
        - [Firebase Storage](https://firebase.google.com/docs/storage)
    """

    def __init__(self, firebase_cred, bucket_name):
        """
        Initializes the FirebaseStorageManager with specified Firebase credentials and bucket name.

        Args:
            firebase_cred (str | dict): The Firebase credentials either as a path to the JSON credentials file or
                a dictionary containing the credentials.
            bucket_name (str): Name of the Firebase storage bucket.

        Returns:
            None

        Example:
            ```python
            firebase_cred = "path/to/firebase/credentials.json"
            bucket_name = "example-bucket"
            storage_manager = FirebaseStorageManager(firebase_cred, bucket_name)
            ```

        References:
            - [Firebase Admin Documentation](https://firebase.google.com/docs/admin/setup)
        """
        self.firebase_cred = firebase_cred
        self.bucket_name = bucket_name
        self._initialize_firebase()

    def _initialize_firebase(self):
        """
        Initializes Firebase app with credentials and sets up storage bucket based on class attributes.

        Args:
            None

        Returns:
            None

        Notes:
            Invoked internally during the instantiation of `FirebaseStorageManager`.

        References:
            [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
        """
        cred = credentials.Certificate(self.firebase_cred)
        firebase_admin.initialize_app(cred, {"storageBucket": self.bucket_name})
        self.bucket = storage.bucket()

    def upload_test_data(self, local_folder, bucket_folder):
        """
        Uploads test data from a local directory to a specified folder in Firebase Storage.

        This method filters and uploads files from the local directory to Firebase Storage, excluding files with patterns
        (".py", "__", ".DS_Store"), keeping the directory structure intact.

        Args:
            local_folder (str): The local directory path containing the files to be uploaded.
            bucket_folder (str): The Firebase Storage folder path where files will be uploaded.

        Returns:
            None

        Example:
            ```python
            local_directory = 'path/to/local/test_data'
            firebase_directory = 'path/in/firebase/test_data'
            firebase_storage_manager.upload_test_data(local_directory, firebase_directory)
            ```

        References:
            - [Firebase Admin SDK: Python](https://firebase.google.com/docs/admin/setup#python)
        """
        files_to_upload = []
        for root, dirs, files in os.walk(local_folder):
            exclude_patterns = [".py", "__", ".DS_Store"]
            files_to_upload.extend(
                os.path.join(root, filename)
                for filename in files
                if all(exclude_pattern not in filename for exclude_pattern in exclude_patterns)
            )
        for local_path in tqdm(files_to_upload, desc="Uploading files", unit="file"):
            relative_path = os.path.relpath(local_path, local_folder)
            firebase_path = os.path.join(bucket_folder, relative_path)

            blob = self.bucket.blob(firebase_path)
            blob.upload_from_filename(local_path)

    def download_test_data(self, bucket_folder, local_folder):
        """
        Downloads test data from Firebase Storage to a local directory.

        This method iterates over the files in the specified Firebase Storage folder and downloads them to the local
        directory, recreating the directory structure as in the storage.

        Args:
            bucket_folder (str): The Firebase Storage folder path from which files will be downloaded.
            local_folder (str): The local directory path where files will be downloaded.

        Returns:
            (None): This function does not return a value.

        Example:
            ```python
            manager = FirebaseStorageManager(firebase_cred='path/to/cred.json', bucket_name='my-bucket')
            manager.download_test_data('test_data_folder', 'local_test_data_folder')
            ```
        """
        blobs = list(self.bucket.list_blobs(prefix=bucket_folder))
        blobs = [blob for blob in blobs if not blob.name.endswith("/")]

        for blob in tqdm(blobs, desc="Downloading files", unit="file"):
            local_file_path = os.path.join(str(local_folder), str(os.path.relpath(blob.name, bucket_folder)))
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            blob.download_to_filename(local_file_path)


def main():
    """
    Main function to either upload or download test data to/from Firebase Storage based on command-line arguments.

    Args:
        None

    Returns:
        None

    Raises:
        ValueError: If the 'FIREBASE_CRED' environment variable is missing.

    Notes:
        This function reads Firebase credentials and bucket name from environment variables 'FIREBASE_CRED' and
        'BUCKET_NAME' respectively. Command-line arguments determine whether files are uploaded to or downloaded
        from Firebase Storage.

    Example:
        To upload files:
        ```bash
        python main.py upload
        ```

        To download files:
        ```bash
        python main.py download
        ```
    """
    base64_cred = os.environ.get("FIREBASE_CRED")
    if base64_cred is None:
        raise ValueError("FIREBASE_CRED environment variable is missing.")

    # Decode the Base64 string
    decoded_cred = base64.b64decode(base64_cred)

    # Convert bytes to string
    decoded_cred_str = decoded_cred.decode("utf-8")

    # Convert to a JSON object (dictionary)
    firebase_cred = json.loads(decoded_cred_str)

    bucket_name = os.environ.get("BUCKET_NAME")
    manager = FirebaseStorageManager(firebase_cred, bucket_name)
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        local_folder = "test_data"
        bucket_folder = "QA/hub-sdk-qa/test_data"
        if command == "upload":
            manager.upload_test_data(local_folder, bucket_folder)
        elif command == "download":
            manager.download_test_data(bucket_folder, local_folder)
        else:
            print("Invalid command. Use 'upload' or 'download'.")
    else:
        print("Please specify a command: 'upload' or 'download'.")


if __name__ == "__main__":
    main()
