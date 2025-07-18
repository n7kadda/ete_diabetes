import logging
import os
from datetime import datetime 

LOGS_DIR = "logs" # Directory to store logs
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, f'log_{datetime.now().strftime("%Y-%m-%d")}.log') # Log file with date in name
logging.basicConfig(
    filename = LOG_FILE, # Log file path
    format = '%(asctime)s - %(levelname)s - %(message)s', # Log format with timestamp, level, and message
    level = logging.INFO # Set logging level to INFO, which captures all messages at this level and above
)

def get_logger(name):
    logger = logging.getLogger(name) # Create a logger with the specified name
    logger.setLevel(logging.INFO) # Set the logger level to INFO
    return logger # Return the configured logger

# This code sets up a logging system that writes logs to a file with a date in the filename, ensuring that logs are organized by day.