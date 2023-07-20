import logging
import os


class PlatformLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        """Add the platform as an extra field in the log records."""
        kwargs["extra"] = kwargs.get("extra", {})
        kwargs["extra"]["platform"] = self.extra["platform"]
        return msg, kwargs


def get_logger(name):
    """Factory method to create a custom logger."""
    logger = logging.getLogger(name)
    formatter = logging.Formatter("[%(levelname)s][%(platform)s][%(username)s] %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(os.getenv("LOG_LEVEL", "ERROR"))
    return PlatformLoggerAdapter(logger, {"platform": name})
