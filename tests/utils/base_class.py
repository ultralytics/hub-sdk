# Ultralytics HUB-SDK 🚀 AGPL-3.0 License - https://ultralytics.com/license

import inspect
import logging
import os
import time

import pytest

from hub_sdk import HUBClient


@pytest.mark.usefixtures("setup")
class BaseClass:
    """Provides base functionality and logging capabilities for classes utilizing the HUBClient SDK."""

    client: HUBClient

    @classmethod
    def get_logger(cls):
        """
        This method creates and configures a custom logger for the calling function or method. It uses the calling
        function's name as the logger name and logs messages to a file located at './reports/logfile.log'.

        Example Usage:
            logger = self.get_logger()
            logger.debug("Debug message")
            logger.info("Information message")
            logger.error("Error message")
        """
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        if not os.path.exists("./reports"):
            os.makedirs("./reports")
        file_handler = logging.FileHandler("./reports/logfile.log")
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.setLevel(logging.DEBUG)
        return logger

    @classmethod
    def delay(cls, seconds=1):
        """Pauses program execution for a given number of seconds."""
        time.sleep(seconds)
