# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import logging
import os


class Logger:
    """
    A class for handling log messages with configurable settings.

    Attributes:
        logger_name (str): Name of the logger. Defaults to the name of the calling module.
        log_format (str): Format for log messages. Defaults to '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                          or the value of the 'LOGGER_FORMAT' environment variable.
        log_level (str): Log level for the logger. Defaults to 'INFO' or the value of the 'LOGGER_LEVEL' environment
                         variable.
        logger (logging.Logger): The configured logger instance.

    Methods:
        __init__: Initialize a Logger instance with optional custom settings.
        get_logger: Retrieve the configured logger instance.

    References:
        - [Python logging documentation](https://docs.python.org/3/library/logging.html)

    Example:
        ```python
        logger = Logger(logger_name='my_logger', log_format='%(name)s - %(levelname)s - %(message)s', log_level='DEBUG')
        log = logger.get_logger()
        log.debug('This is a debug message')
        ```
    """

    def __init__(self, logger_name=None, log_format=None, log_level=None):
        """
        Initializes a Logger instance with specified configuration.

        Args:
            logger_name (str | None): Name of the logger. If None, defaults to the current module's name.
            log_format (str | None): Format for log messages. Defaults to 'LOGGER_FORMAT' environment variable or
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'.
            log_level (str | None): Log level for the logger. Defaults to 'LOGGER_LEVEL' environment variable or 'INFO'.

        Notes:
            The logger configuration defaults to environment variables if not explicitly provided.

        References:
            [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
        """
        self.log_format = log_format or os.environ.get(
            "LOGGER_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.log_level = log_level or os.environ.get("LOGGER_LEVEL", "INFO")
        self.logger_name = logger_name or __name__

        self.logger = self._configure_logger()

    def _configure_logger(self) -> logging.Logger:
        """
        Configures the logger with specified name, format, and logging level.

        Returns:
            (logging.Logger): A configured logger instance with the specified name, format, and logging level.

        Notes:
            The logger format and level can be customized via the 'LOGGER_FORMAT' and 'LOGGER_LEVEL' environment
            variables respectively.

        References:
            - [Logging facility for Python](https://docs.python.org/3/library/logging.html)
        """
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)

        formatter = logging.Formatter(self.log_format)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            (logging.Logger): The configured logger instance.

        Example:
            ```python
            logger = Logger().get_logger()
            logger.info("This is an info message.")
            ```
        """
        return self.logger


logger = Logger().get_logger()
