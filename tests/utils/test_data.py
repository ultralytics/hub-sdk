import base64
import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from tqdm import tqdm
import sys


class FirebaseStorageManager:
    def __init__(self, firebase_cred, bucket_name):
        self.firebase_cred = firebase_cred
        self.bucket_name = bucket_name
        self._initialize_firebase()

    def _initialize_firebase(self):
        cred = credentials.Certificate(self.firebase_cred)
        firebase_admin.initialize_app(cred, {"storageBucket": self.bucket_name})
        self.bucket = storage.bucket()

    def upload_test_data(self, local_folder, bucket_folder):
        """
        Uploads test data from a local directory to a specified folder in Firebase Storage.

        This method scans through all the files in the local directory (excluding file containing ".py","__",".DS_Store"
        ) and uploads them to the defined path in Firebase Storage, maintaining the directory structure.

        Args:
            local_folder (str): The local directory path containing the files to be uploaded.
            bucket_folder (str): The Firebase Storage folder path where files will be uploaded.
        """
        files_to_upload = []
        for root, dirs, files in os.walk(local_folder):
            exclude_patterns = [".py", "__", ".DS_Store"]
            for filename in files:
                if any(exclude_pattern in filename for exclude_pattern in exclude_patterns):
                    continue
                files_to_upload.append(os.path.join(root, filename))

        for local_path in tqdm(files_to_upload, desc="Uploading files", unit="file"):
            relative_path = os.path.relpath(local_path, local_folder)
            firebase_path = os.path.join(bucket_folder, relative_path)

            blob = self.bucket.blob(firebase_path)
            blob.upload_from_filename(local_path)

    def download_test_data(self, bucket_folder, local_folder):
        """
        Downloads test data from Firebase Storage to a local directory.

        This method iterates over the files in the specified Firebase Storage folder and downloads them
        to the local directory, recreating the directory structure as in the storage.

        Args:
            bucket_folder (str): The Firebase Storage folder path from which files will be downloaded.
            local_folder (str): The local directory path where files will be downloaded.
        """
        blobs = list(self.bucket.list_blobs(prefix=bucket_folder))
        blobs = [blob for blob in blobs if not blob.name.endswith("/")]

        for blob in tqdm(blobs, desc="Downloading files", unit="file"):
            local_file_path = os.path.join(str(local_folder), str(os.path.relpath(blob.name, bucket_folder)))
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            blob.download_to_filename(local_file_path)


def main():
    # Decoding the Base64 encoded Firebase credentials
    base64_cred = os.environ.get("FIREBASE_CRED")
    if base64_cred is None:
        raise ValueError("FIREBASE_CRED environment variable is missing.")

    # Decode the Base64 string
    decoded_cred = base64.b64decode(base64_cred)

    # Convert to a JSON object (dictionary)
    firebase_cred = json.loads(decoded_cred)

    bucket_name = os.environ.get("BUCKET_NAME")
    manager = FirebaseStorageManager(firebase_cred, bucket_name)
    local_folder = "test_data"
    bucket_folder = "QA/hub-sdk-qa/test_data"
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
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
