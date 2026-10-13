import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////myapp/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model to store prediction history
class PredictionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    prediction_result = db.Column(db.String(50), nullable=False)

# Ensure database tables exist
with app.app_context():
    os.makedirs("/myapp/instance", exist_ok=True)
    db.create_all()

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    try:
        record = PredictionRecord(
            sepal_length=data["sepal_length"],
            sepal_width=data["sepal_width"],
            petal_length=data["petal_length"],
            petal_width=data["petal_width"],
            prediction_result=data["prediction_result"]
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/records", methods=["GET"])
def get_records():
    try:
        records = PredictionRecord.query.all()
        result = [
            {
                "id": r.id,
                "sepal_length": r.sepal_length,
                "sepal_width": r.sepal_width,
                "petal_length": r.petal_length,
                "petal_width": r.petal_width,
                "prediction_result": r.prediction_result
            } for r in records
        ]
        return jsonify({"status": "success", "records": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
