# This code is part of a machine learning project for diabetes classification.
# It includes a class for training a LightGBM model with hyperparameter tuning using RandomizedSearchCV.
# The module is designed to work with a specific dataset related to diabetes.
import os
import re 
import numpy as np 
import pandas as pd
import joblib
import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
import warnings
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import load_data, read_yaml

# Initialize logger
logger = get_logger(__name__)
warnings.filterwarnings("ignore", category=UserWarning, module="lightgbm")


class ModelTraining: # Class for model training


    def __init__(self, config_path: str): # Initialize the ModelTraining class with configuration path
        self.config = read_yaml(config_path) # Read configuration from YAML file
        self.train_path = PROCESSED_TRAIN_DATA_PATH # Path to the processed training data file
        self.test_path = PROCESSED_TEST_DATA_PATH # Path to the processed test data file
        self.model_output_path = MODEL_OUTPUT_PATH # Path to save the trained model
        self.target_column = self.config['data_preprocessing']['target_column'] # Target column for prediction
        self.param_dist = LIGHTGM_PARAMS # Hyperparameter distribution for RandomizedSearchCV
        self.random_search_params = RANDOM_SEARCH_PARAMS # Parameters for RandomizedSearchCV
        logger.info("ModelTraining class initialized successfully.")

    def load_processed_data(self) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:

        try:
            logger.info(f"Loading processed training data from: {self.train_path}") 
            train_df = load_data(self.train_path) # Load processed training data
            logger.info(f"Loading processed test data from: {self.test_path}")
            test_df = load_data(self.test_path) # Load processed test data

            for df in [train_df, test_df]:
                if 'Unnamed: 0' in df.columns: 
                    df.drop(columns=['Unnamed: 0'], inplace=True)
                    logger.info("Dropped 'Unnamed: 0' column.")

            logger.info("Sanitizing column names for LightGBM compatibility.")
            sanitized_columns = {col: re.sub(r'[^A-Za-z0-9_]+', '', col) for col in train_df.columns}
            train_df = train_df.rename(columns=sanitized_columns)
            test_df = test_df.rename(columns=sanitized_columns)
            
            sanitized_target_column = re.sub(r'[^A-Za-z0-9_]+', '', self.target_column)
            logger.info("Column names sanitized.")

            logger.info("Separating features (X) and target (y).")
            X_train = train_df.drop(columns=[sanitized_target_column]) # Features for training data
            y_train = train_df[sanitized_target_column] # Target for training data
            X_test = test_df.drop(columns=[sanitized_target_column]) # Features for test data
            y_test = test_df[sanitized_target_column] # Target for test data

            logger.info("Processed data loaded and split successfully.")
            return X_train, y_train, X_test, y_test # Return features and target for both train and test sets

        except Exception as e:
            logger.error(f"An unexpected error occurred while loading processed data: {e}")
            raise CustomException("Failed to load processed data", e)

    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> lgb.LGBMClassifier:

        try:
            logger.info("Starting model training with LightGBM and RandomizedSearchCV.")

            # Initialize LightGBM model with default parameters
            neg_count = y_train.value_counts()[0] # Count of negative class
            pos_count = y_train.value_counts()[1] # Count of positive class
            scale_pos_weight = neg_count / pos_count # Calculate scale_pos_weight for handling class imbalance
            logger.info(f"Calculated scale_pos_weight for class imbalance: {scale_pos_weight:.2f}")

            # Pass the parameter to the model
            lgbm_model = lgb.LGBMClassifier( # Initialize LightGBM model
                random_state=self.random_search_params.get("random_state", 42), 
                scale_pos_weight=scale_pos_weight # Handle class imbalance
            )

            random_search = RandomizedSearchCV( # Initialize RandomizedSearchCV
                estimator=lgbm_model,
                param_distributions=self.param_dist,
                n_iter=self.random_search_params["n_iter"],
                cv=self.random_search_params["cv"],
                n_jobs=self.random_search_params.get("n_jobs", -1),
                verbose=self.random_search_params.get("verbose", 1),
                random_state=self.random_search_params.get("random_state", 42),
                scoring=self.random_search_params["scoring"]
            )

            logger.info("Fitting RandomizedSearchCV to the training data...")
            random_search.fit(X_train, y_train) # Fit the model using RandomizedSearchCV
            
            best_params = random_search.best_params_ # Get the best hyperparameters from the search
            best_lgbm_model = random_search.best_estimator_ # Get the best model from the search

            logger.info(f"Model training completed. Best hyperparameters found: {best_params}")
            mlflow.log_params(best_params) # Log the best hyperparameters to MLflow
            # Log our calculated scale_pos_weight as well for traceability
            mlflow.log_param("scale_pos_weight", scale_pos_weight) # Log scale_pos_weight to MLflow
            return best_lgbm_model # Return the best trained model

        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise CustomException("Model training failed", e)

    def evaluate_model(self, model: lgb.LGBMClassifier, X_test: pd.DataFrame, y_test: pd.Series):

        try:
            logger.info("Evaluating the trained model on the test data.")
            y_pred = model.predict(X_test) # Predict on the test set
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred),
                "recall": recall_score(y_test, y_pred),
                "f1_score": f1_score(y_test, y_pred)
            }
            logger.info(f"Evaluation Metrics: {metrics}")
            mlflow.log_metrics(metrics)
        except Exception as e:
            logger.error(f"Error while evaluating model: {e}")
            raise CustomException("Failed to evaluate model", e)

    def run(self):

        logger.info("Starting the model training pipeline run.")
        try:
            with mlflow.start_run(): # Start an MLflow run
                mlflow.set_tag("PipelineStep", "ModelTraining") # Set a tag for the MLflow run
                logger.info(f"MLflow run started. Run ID: {mlflow.active_run().info.run_id}")

                X_train, y_train, X_test, y_test = self.load_processed_data() # Load processed data
                mlflow.log_param("training_data_path", self.train_path) # Log training data path
                mlflow.log_param("test_data_path", self.test_path) # Log test data path

                best_lgbm_model = self.train_model(X_train, y_train) # Train the model
                self.evaluate_model(best_lgbm_model, X_test, y_test) # Evaluate the trained model

                logger.info("Logging model to MLflow Model Registry.")
                mlflow.sklearn.log_model( # Log the trained model to MLflow
                    sk_model=best_lgbm_model, # Use the best model from RandomizedSearchCV
                    artifact_path="model", # Path in MLflow where the model will be stored
                    registered_model_name="LightGBM_Diabetes_Classifier" # Name of the registered model in MLflow
                )
                logger.info("Model successfully logged to MLflow.")
                
                os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
                joblib.dump(best_lgbm_model, self.model_output_path)
                logger.info(f"Model artifact also saved locally to {self.model_output_path}")

                logger.info("Model training pipeline run completed successfully.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during the pipeline run: {e}")
            raise

if __name__ == "__main__":
    logger.info("Executing model_training.py as a standalone script.")
    try:
        model_trainer = ModelTraining(config_path=CONFIG_PATH)
        model_trainer.run()
    except Exception as e:
        logger.critical(f"The model training script failed to run. Error: {e}")

