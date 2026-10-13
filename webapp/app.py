import os
import pickle
import requests
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

MODEL_PATH = os.path.join("models", "gaussian_nb_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

DBAPP_URL = os.environ.get("DBAPP_URL", "http://localhost:5001")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    try:
        if request.method == "GET":
            return redirect(url_for("index"))

        sepal_length = float(request.form["sepal_length"])
        sepal_width = float(request.form["sepal_width"])
        petal_length = float(request.form["petal_length"])
        petal_width = float(request.form["petal_width"])
    except (KeyError, ValueError):
        return render_template(
            "result.html",
            prediction="Invalid input. Please enter valid numbers for all fields.",
            inputs=None,
        )
    features = [[sepal_length, sepal_width, petal_length, petal_width]]
    prediction = model.predict(features)[0]
    
    # Save the prediction to the database via dbapp API
    try:
        requests.post(f"{DBAPP_URL}/save", json={
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width,
            "prediction_result": str(prediction)
        }, timeout=5)
    except Exception as e:
        print(f"Error saving to dbapp: {e}")

    inputs = {
        "Sepal Length": sepal_length,
        "Sepal Width": sepal_width,
        "Petal Length": petal_length,
        "Petal Width": petal_width,
    }

    return render_template("result.html", prediction=prediction, inputs=inputs)

@app.route("/records", methods=["GET"])
def records():
    try:
        response = requests.get(f"{DBAPP_URL}/records", timeout=5)
        response_data = response.json()
        records_list = response_data.get("records", [])
    except Exception as e:
        print(f"Error fetching from dbapp: {e}")
        records_list = []
        
    return render_template("records.html", records=records_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
