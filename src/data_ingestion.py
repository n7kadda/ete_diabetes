import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
from google.cloud import storage
from sklearn.model_selection import train_test_split
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)  # Initialize logger

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"] # Load data ingestion configuration
        self.bucket_name = self.config["bucket_name"] # Name of the GCP bucket
        self.bucket_file_name = self.config["bucket_file_name"] # Name of the file in the bucket
        self.train_test_ratio = self.config["train_ratio"] # Ratio of training data

        os.makedirs(RAW_DIR, exist_ok=True)  # Create raw directory if it doesn't exist

        logger.info(f"Data Ingestion started with {self.bucket_name} bucket and file {self.bucket_file_name}")  # Log start of data ingestion

    def download_data(self):
        try:
            client = storage.Client() # Initialize GCP storage client
            bucket = client.bucket(self.bucket_name) # Picks a bucket (the folder in gcp where your files are stored) using its name
            blob = bucket.blob(self.bucket_file_name) # Picks a file in the bucket using its name

            blob.download_to_filename(RAW_FILE_PATH) # Downloads the file to the specified path
            logger.info(f"Data downloaded from bucket {self.bucket_name} to {RAW_FILE_PATH}")  # Log successful download
        
        except Exception as e:
            logger.error("Error while downloading data from GCP bucket")
            raise CustomException("Failed to download data from GCP bucket", e) 
    
    def split_data(self):
        try:
            logger.info("Splitting data into train and test sets")  # Log start of data splitting
            data = pd.read_csv(RAW_FILE_PATH)  # Read the raw data file
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)  # Split data into train and test sets

            train_data.to_csv(TRAIN_FILE_PATH) # Save training data to file
            test_data.to_csv(TEST_FILE_PATH) # Save test data to file
            logger.info(f"Data split completed. Train data saved to {TRAIN_FILE_PATH} and test data saved to {TEST_FILE_PATH}")  # Log successful data splitting

        except Exception as e:
            logger.error("Error while splitting data into train and test sets")
            raise CustomException("Failed to split data into train and test sets", e)  # Raise custom exception with error message and original exception
    
    def run(self):
        try:
            logger.info("Starting data ingestion process")  # Log start of data ingestion process
            self.download_data() # Download data from GCP bucket
            self.split_data() # Split data into train and test sets
            logger.info("Data ingestion process completed successfully")  # Log successful completion of data ingestion process
        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}") # Log custom exception message

        finally:
            logger.info("Data ingestion process finished") # Log end of data ingestion process

if __name__ == "__main__":
    data_injestion = DataIngestion(read_yaml(CONFIG_PATH))  # Initialize DataIngestion with configuration
    data_injestion.run()  # Run the data ingestion process
    