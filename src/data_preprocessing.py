# This code is part of a data preprocessing module for a machine learning project.
# It includes functions for loading data, feature engineering, handling missing values and scaling,
# and saving processed data. The module is designed to work with a specific dataset related to diabetes.
import os
import pandas as pd
import joblib
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import read_yaml, load_data
from config.paths_config import *

logger = get_logger(__name__)

class DataPreprocessor: # Class for data preprocessing
    def __init__(self, config_path):    # Initialize the DataPreprocessor with configuration
        self.config = read_yaml(config_path) # Read configuration from YAML file
        self.preprocessing_config = self.config['data_preprocessing'] # Load preprocessing configuration
        self.numerical_columns = self.preprocessing_config['numerical_columns'] # List of numerical columns to be processed
        self.target_column = self.preprocessing_config['target_column'] # Target column for prediction
        
        self.train_path = TRAIN_FILE_PATH # Path to the training data file
        self.test_path = TEST_FILE_PATH # Path to the test data file
        self.processed_dir = PROCESSED_DIR # Directory where processed data files will be stored

        os.makedirs(self.processed_dir, exist_ok=True)
        logger.info("DataPreprocessor initialized.")

    def create_features(self, df: pd.DataFrame) -> pd.DataFrame: # Function to create new features from existing ones

        logger.info("Starting feature engineering.")  
        # Create interaction features
        df['Glucose_x_BMI'] = df['Glucose'] * df['BMI'] # Interaction between Glucose and BMI
        df['Glucose_x_Age'] = df['Glucose'] * df['Age'] # Interaction between Glucose and Age
        df['SkinThickness_x_Insulin'] = df['SkinThickness'] * df['Insulin'] # Interaction between SkinThickness and Insulin
        logger.info(f"Created new features: {['Glucose_x_BMI', 'Glucose_x_Age', 'SkinThickness_x_Insulin']}")
        return df

    def process(self): # Main function to process the data

        try:
            logger.info("Starting full data preprocessing pipeline.")

            # 1. Load raw data
            train_df = load_data(self.train_path) # Load training data
            test_df = load_data(self.test_path) # Load test data
            logger.info("Raw train and test data loaded successfully.")

            # 2. <<< NEW STEP: Feature Engineering >>>
            train_df = self.create_features(train_df) # Create new features for training data
            test_df = self.create_features(test_df) # Create new features for test data

            # 3. Separate features and target
            X_train = train_df.drop(columns=[self.target_column]) # Features for training data
            y_train = train_df[[self.target_column]] # Target for training data
            X_test = test_df.drop(columns=[self.target_column]) # Features for test data 
            y_test = test_df[[self.target_column]] # Target for test data

            # 4. Handle Missing Values
            logger.info("Starting missing value imputation.")
            imputer = SimpleImputer(strategy='mean') # Initialize imputer to fill missing values with mean
            X_train[self.numerical_columns] = imputer.fit_transform(X_train[self.numerical_columns]) # Fit and transform training data
            X_test[self.numerical_columns] = imputer.transform(X_test[self.numerical_columns]) # Transform test data
            logger.info("Missing values handled successfully.")

            # 5. Scale Numerical Features
            logger.info("Starting data scaling using RobustScaler.")
            scaler = RobustScaler() # Initialize scaler to scale numerical features
            X_train[self.numerical_columns] = scaler.fit_transform(X_train[self.numerical_columns]) # Fit and transform training data
            X_test[self.numerical_columns] = scaler.transform(X_test[self.numerical_columns]) # Transform test data
            logger.info("Data scaling completed.") 

            # 6. Save the fitted scaler
            scaler_path = os.path.join(self.processed_dir, 'scaler.joblib')
            joblib.dump(scaler, scaler_path) # Save the fitted scaler to a file
            logger.info(f"Fitted scaler saved to {scaler_path}")

            # 7. Re-combine and save final data
            processed_train_df = pd.concat([X_train, y_train], axis=1) # Combine features and target for training data
            processed_test_df = pd.concat([X_test, y_test], axis=1) # Combine features and target for test data
            self.save_data(processed_train_df, PROCESSED_TRAIN_DATA_PATH) # Save processed training data
            self.save_data(processed_test_df, PROCESSED_TEST_DATA_PATH) # Save processed test data

            logger.info("Data preprocessing pipeline completed successfully.")

        except Exception as e:
            logger.error(f"An unexpected error occurred in the preprocessing pipeline: {e}")
            raise CustomException("Unexpected error in preprocessing pipeline", e)

    def save_data(self, df: pd.DataFrame, file_path: str): # Function to save processed data to a file
        try:
            df.to_csv(file_path, index=False) # Save DataFrame to CSV file without index
            logger.info(f"Data saved successfully to {file_path}")
        except Exception as e:
            logger.error(f"Error while saving data to {file_path}: {e}")
            raise CustomException("Failed to save processed data", e)

if __name__ == "__main__":
    try:
        preprocessor = DataPreprocessor(config_path=CONFIG_PATH)
        preprocessor.process()
    except Exception as e:
        logger.critical(f"The data preprocessing script failed to run. Error: {e}")
