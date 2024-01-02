import logging
import os


class Logger:
    def __init__(self, logger_name=None, log_format=None, log_level=None):
        """
        Initialize a Logger instance.

        Args:
            logger_name (str): Name of the logger. If not provided, defaults to the root logger.
            log_format (str): Format for log messages. Defaults to the value of 'LOGGER_FORMAT'
                             environment variable or '%(asctime)s - %(levelname)s - %(message)s'.
            log_level (str): Log level for the logger. Defaults to the value of 'LOGGER_LEVEL'
                            environment variable or 'INFO'.
        """
        self.log_format = log_format or os.environ.get(
            "LOGGER_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.log_level = log_level or os.environ.get("LOGGER_LEVEL", "INFO")
        self.logger_name = logger_name or __name__

        self.logger = self._configure_logger()

    def _configure_logger(self):
        """
        Configure the logger with the provided settings.

        Returns:
            logging.Logger: A configured logger instance.
        """
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)

        formatter = logging.Formatter(self.log_format)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    def get_logger(self) -> None:
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger


logger = Logger().get_logger()
