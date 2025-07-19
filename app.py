import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, render_template

# This code is part of a Flask web application that serves a machine learning model for diabetes prediction.
# It includes routes for the home page and a prediction endpoint.
app = Flask(__name__)  # Initialize Flask application

MODEL_PATH = os.path.join('artifacts', 'models', 'lgmb_model.pkl') # Path to the trained model
SCALER_PATH = os.path.join('artifacts', 'processed', 'scaler.joblib') # Path to the scaler used for feature scaling

try:
    # Load the pre-trained model and scaler
    model = joblib.load(MODEL_PATH) # Load the LightGBM model
    scaler = joblib.load(SCALER_PATH) # Load the scaler for feature scaling
    print("Model and scaler loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading artifacts: {e}. Make sure the paths are correct and artifacts exist.")
    model = None
    scaler = None
except Exception as e:
    print(f"An unexpected error occurred during artifact loading: {e}")
    model = None
    scaler = None

@app.route('/', methods=['GET']) # Home route
def home(): # Render the home page
    return render_template('index.html', prediction_text='') # Render the home page with an empty prediction text

@app.route('/predict', methods=['POST']) # Prediction route
def predict(): # Handle prediction requests
    if model is None or scaler is None:
        return render_template('index.html', prediction_text='Error: Model or scaler not loaded.')
    try:
        form_features = [float(x) for x in request.form.values()] # Get form data and convert to float
        feature_names = [ 
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ] # Define feature names
        input_df = pd.DataFrame([form_features], columns=feature_names) # Create DataFrame from input features
        input_df['Glucose_x_BMI'] = input_df['Glucose'] * input_df['BMI'] # Create interaction feature
        input_df['Glucose_x_Age'] = input_df['Glucose'] * input_df['Age'] # Create interaction feature
        input_df['SkinThickness_x_Insulin'] = input_df['SkinThickness'] * input_df['Insulin'] # Create interaction feature
        
        scaled_features = scaler.transform(input_df) # Scale the features using the loaded scaler
        prediction = model.predict(scaled_features)     # Make prediction using the loaded model
        prediction_proba = model.predict_proba(scaled_features) # Get prediction probabilities

        if prediction[0] == 1: # If the prediction is for 'Diabetic'
            # Get the confidence score for the 'Diabetic' class
            confidence = prediction_proba[0][1] * 100
            output_text = f"Prediction: Diabetic (Confidence: {confidence:.2f}%)"
        else:
            # Get the confidence score for the 'Not Diabetic' class
            confidence = prediction_proba[0][0] * 100
            output_text = f"Prediction: Not Diabetic (Confidence: {confidence:.2f}%)"

    except Exception as e:
        output_text = f"An error occurred during prediction: {e}"

    # Render the page again, this time with the prediction result
    return render_template('index.html', prediction_text=output_text)

if __name__ == '__main__':
    if model is None or scaler is None:
        print("Model or scaler not loaded. Exiting the application.")
    else:
        app.run(debug=True)  # Run the Flask app in debug mode



