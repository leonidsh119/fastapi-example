import logging
import sys

def setup_logging():
    """Set up the logging configuration."""
    # Create a custom logger
    logger = logging.getLogger()

    # Set the default logging level
    logger.setLevel(logging.INFO)

    # Create console handler and set its level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger
