import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

# Get the root logger
logger = logging.getLogger("NextStep-AI Logger")
logger.setLevel(logging.INFO)

# Prevent adding handlers multiple times
if not logger.handlers:
    # Create a formatter
    formatter = logging.Formatter(logging_str)

    # File handler with UTF-8 encoding
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console stream handler with error replacement
    # This is a robust way to handle potential encoding issues on Windows
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except TypeError:
            # In some environments (like certain IDEs), reconfigure might not be available.
            # The default error handler will be used.
            pass
    logger.addHandler(stream_handler)
