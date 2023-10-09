from setuptools import setup, find_packages

import re
from pathlib import Path

import pkg_resources as pkg

# Settings
FILE = Path(__file__).resolve()
PARENT = FILE.parent  # root directory
README = (PARENT / "README.md").read_text(encoding="utf-8")
REQUIREMENTS = [
    f"{x.name}{x.specifier}"
    for x in pkg.parse_requirements((PARENT / "requirements.txt").read_text())
]


def get_version():
    file = PARENT / "hub_sdk/__init__.py"
    return re.search(
        r'^__version__ = [\'"]([^\'"]*)[\'"]', file.read_text(encoding="utf-8"), re.M
    )[1]


setup(
    name="hub_sdk",
    version=get_version(),
    python_requires=">=3.8",
    author="Ultralytics",
    author_email="hello@ultralytics.com",
    description="Ultralytics HUB Client SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ultralytics/hub-sdk",
    project_urls={
        "Bug Reports": "https://github.com/ultralytics/hub/issues",
        "Funding": "https://ultralytics.com",
        "Source": "https://github.com/ultralytics/hub-sdk",
    },
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    keywords="machine-learning, deep-learning, vision, ML, DL, AI, YOLO, YOLOv3, YOLOv5, YOLOv8, HUB, Ultralytics",
)
