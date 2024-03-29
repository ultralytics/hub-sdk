import inspect
import logging
import os
import time
import pytest
from hub_sdk import HUBClient


@pytest.mark.usefixtures("setup")
class BaseClass:
    client: HUBClient

    @classmethod
    def getLogger(cls):
        """
        This method creates and configures a custom logger for the calling function or method. It uses the calling
        function's name as the logger name and logs messages to a file located at './reports/logfile.log'.

        Example Usage:
            logger = self.getLogger()
            logger.debug("Debug message")
            logger.info("Information message")
            logger.error("Error message")
        """
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        if not os.path.exists("./reports"):
            os.makedirs("./reports")
        fileHandler = logging.FileHandler("./reports/logfile.log")
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)

        logger.setLevel(logging.DEBUG)
        return logger

    @classmethod
    def delay(cls, seconds=1):
        time.sleep(seconds)
