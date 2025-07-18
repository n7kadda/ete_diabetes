import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__) # Initialize logger

def read_yaml(file_path): # Function to read a YAML file
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in the given path") # Check if the file exists
        
        with open(file_path,"r") as yaml_file: # Open the YAML file in read mode
            config = yaml.safe_load(yaml_file) # Load the YAML file content
            logger.info("Succesfully read the YAML file") # Log success message
            return config # Return the loaded configuration
    
    except Exception as e: # Handle exceptions
        logger.error("Error while reading YAML file") # Log error message
        raise CustomException("Failed to read YAMl file" , e) # Raise custom exception with error message and original exception

def load_data(path):
    try:
        logger.info(f"Loading data from {path}") # Log the data loading process
        return pd.read_csv(path) # Read and return the CSV data as a DataFrame
    except Exception as e: # Handle exceptions
        logger.error(f"Error while loading data {e}")
        raise CustomException("Failed to load data", e) # Raise custom exception with error message and original exception