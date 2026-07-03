import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# Load model dan scaler
with open('model.pkl', 'rb') as f:
    models = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# models[0] = Decision Tree, models[1] = SVC
model_dt  = models[0]
model_svc = models[1]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [
            float(request.form['Pregnancies']),
            float(request.form['Glucose']),
            float(request.form['BloodPressure']),
            float(request.form['SkinThickness']),
            float(request.form['Insulin']),
            float(request.form['BMI']),
            float(request.form['DiabetesPedigreeFunction']),
            float(request.form['Age']),
        ]

        algo = request.form.get('algorithm', 'dt')
        model = model_svc if algo == 'svc' else model_dt

        data_scaled = scaler.transform([data])
        prediction  = model.predict(data_scaled)

        result = 'Positif Diabetes' if prediction[0] == 1 else 'Negatif Diabetes'

    except Exception as e:
        result = f'Error: {str(e)}'

    return render_template('index.html', prediction_text=result)

if __name__ == '__main__':
    app.run(debug=True)