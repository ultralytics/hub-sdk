import inspect
import logging
import os
import time

import pytest
from hub_sdk import HUBClient


@pytest.mark.usefixtures("setup")
class BaseClass:
    """
    A foundational class in the Ultralytics library that provides basic utilities including logging and delay
    functionality.

    Attributes:
        client (HUBClient): The HUBClient instance used for interacting with a remote server or service.

    Methods:
        get_logger: Configures a custom logger for the calling function or method.
        delay: Pauses program execution for a given number of seconds.

    Example:
        ```python
        base = BaseClass()
        logger = base.get_logger()
        logger.info("Starting process")
        base.delay(seconds=2)
        logger.info("Process completed")
        ```

    References:
        [Logging Documentation](https://docs.python.org/3/library/logging.html)
        [time.sleep Documentation](https://docs.python.org/3/library/time.html#time.sleep)
    """

    client: HUBClient

    @classmethod
    def get_logger(cls):
        """
        Creates and configures a custom logger for the calling function or method.

        Args:
            None

        Returns:
            (logging.Logger): Configured logger instance for the calling function or method.

        Example:
            ```python
            class SomeClass(BaseClass):
                def some_method(self):
                    logger = self.get_logger()
                    logger.info("Info message")
                    logger.error("Error message")
            ```

        Notes:
            Logs messages to a file located at './reports/logfile.log'.

        References:
            [logging](https://docs.python.org/3/library/logging.html#logging.Logger)
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
        """
        Pauses program execution for a given number of seconds.

        Args:
            seconds (int | float, optional): Number of seconds to pause execution. Defaults to 1.

        Returns:
            (None): This method does not return a value.

        Example:
            ```python
            BaseClass.delay(2)  # Pauses execution for 2 seconds
            ```

        Notes:
            The delay function can be useful for simulating network latency or waiting for asynchronous operations to complete.
        """
        time.sleep(seconds)
