from setuptools import setup, find_packages

setup(
    name="hub_client",
    version="0.0.1",
    author="",
    author_email="",
    description="Description of your package",
    packages=find_packages(where="src"),
    package_dir = {"": "src"}
)

