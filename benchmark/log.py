import os
import inspect
import logging
import pprint
import datetime
from typing import Optional

logger: Optional[logging.Logger] = None


def log_name():
    """Get the name and file of the function that called the current function."""
    frame = inspect.stack()[1]
    function_name = frame[3]
    filename = os.path.basename(frame[1])

    base_filename = os.path.splitext(filename)[0]
    log_name = f"{base_filename}_{function_name}.log"
    return log_name


def init_logger(log_dir, log_file, add_timestamp=False):
    """
    Configure the logger with the given log file.

    Args:
    - log_dir (str): The directory to store the log file.
    - log_file (str): The name of the log file.
    - add_timestamp (bool): If True, append a timestamp to the log file name.
    """
    global logger

    # Ensure the directory exists
    os.makedirs(log_dir, exist_ok=True)

    if add_timestamp:
        # Extract the file extension if present
        file_name, file_extension = os.path.splitext(log_file)

        # Generate a timestamp string
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Combine file name, timestamp, and extension
        log_file = f"{file_name}_{timestamp}{file_extension}"

    log_file = os.path.join(log_dir, log_file)

    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        handlers=[logging.StreamHandler(),
                                  logging.FileHandler(log_file, "a")])
    logger = logging.getLogger(__name__)


def log(data, pretty=False):
    """
    Print and log the data.

    Args:
    - data (str or any): The data to be printed and logged. If it's not a string and pretty=True, it will be pretty printed.
    - pretty (bool): If True, pretty-print the data. If data is a string, it will be printed as-is regardless of this flag.
    """
    global logger
    if pretty and not isinstance(data, str):
        output = pprint.pformat(data)
    else:
        output = str(data)

    # Only log if the logger has been initialized
    if logger:
        logger.info(output)
    else:
        raise Exception(
            "Logger has not been initialized. "
            "Please call init_logger() first."
        )


def header(content, width=50, char="-", surround=(' ', ' ')) -> str:
    """Format a print line with consistent width and centered content."""

    # Surround the content with the given characters
    content = f"{surround[0]}{content}{surround[1]}"

    padding = width - len(content)
    left_padding = padding // 2
    right_padding = padding - left_padding

    # construct the final string with the padding and content
    formatted = f"{char * left_padding}{content}{char * right_padding}"
    return formatted
