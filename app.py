from flask import Flask, render_template, request
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the trained KNN model and scaler
knn_model = joblib.load('knn_model.pkl')  # Ensure this path is correct
scaler = joblib.load('scaler.pkl')  # Ensure this path is correct

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from form
    precipitation = float(request.form['precipitation'])
    temp_max = float(request.form['temp_max'])
    temp_min = float(request.form['temp_min'])
    wind = float(request.form['wind'])

    # Prepare input data for prediction
    input_data = np.array([[precipitation, temp_max, temp_min, wind]])
    scaled_input = scaler.transform(input_data)  # Scaler expects only 4 features

    # Predict weather
    prediction = knn_model.predict(scaled_input)

    # Map prediction result to weather category
    weather_map = {0: 'Drizzle', 1: 'Fog', 2: 'Rain', 3: 'Snow', 4: 'Sun'}
    predicted_weather = weather_map[prediction[0]]

    return render_template('index.html', prediction=predicted_weather)

if __name__ == '__main__':
    app.run(debug=True)
