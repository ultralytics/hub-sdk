import logging
import os

class Logger:
    def __init__(self, logger_name=None, log_format=None, log_level=None):
        self.log_format = log_format or os.environ.get('LOGGER_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')
        self.log_level = log_level or os.environ.get('LOGGER_LEVEL', 'INFO')
        self.logger_name = logger_name

        self.logger = self._configure_logger()

    def _configure_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)

        formatter = logging.Formatter(self.log_format)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    def get_logger(self):
        return self.logger
