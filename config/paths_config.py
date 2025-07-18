# This file contains the configuration paths for the project.
# It defines the paths for raw data, processed data, and configuration files.
import os

RAW_DIR = "artifacts/raw" # Directory where raw data files are stored
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw_data.csv") # Path to the raw data file
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train_data.csv") # Path to the training data file 
TEST_FILE_PATH = os.path.join(RAW_DIR, "test_data.csv") # Path to the test data file
CONFIG_PATH = "config/config.yaml" # Path to the configuration file


PROCESSED_DIR = "artifacts/processed" # Directory where processed data files are stored
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv") # Path to the processed training data file
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv") # Path to the processed test data file

MODEL_OUTPUT_PATH = "artifacts/models/lgmb_model.pkl" # Directory where model output files are store
