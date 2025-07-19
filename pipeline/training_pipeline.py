# This code is part of a training pipeline for a machine learning project.
# It orchestrates the data ingestion, preprocessing, and model training steps.
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.paths_config import *

if __name__ == "__main__":

    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()  # Start the data ingestion process

    preprocessor = DataPreprocessor(config_path=CONFIG_PATH)
    preprocessor.process()
    preprocessor.process() # Start the data preprocessing pipeline
    model_trainer = ModelTraining(config_path=CONFIG_PATH)
    model_trainer.run()