from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

app = Flask(__name__)

# Train model if not already saved
MODEL_PATH = 'model.pkl'
if not os.path.exists(MODEL_PATH):
    data = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv")
    X = data.drop("medv", axis=1)
    y = data["medv"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print("RMSE:", rmse)
    joblib.dump(model, MODEL_PATH)

# Load model
model = joblib.load(MODEL_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [float(x) for x in request.form.values()]
        final_features = np.array([features])
        prediction = model.predict(final_features)
        return render_template('index.html', prediction_text=f'Predicted House Price: ${prediction[0]*1000:.2f}')
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
