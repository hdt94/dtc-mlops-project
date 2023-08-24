import os

from flask import Flask, jsonify, request, render_template
import mlflow


MLFLOW_MODEL_URI = os.getenv('MLFLOW_MODEL_URI', None)
assert MLFLOW_MODEL_URI is not None, "Missing MLFLOW_MODEL_URI"

MLFLOW_MODEL_VERSION = os.getenv('MLFLOW_MODEL_VERSION', None)


app = Flask('duration-prediction')
model = mlflow.pyfunc.load_model(MLFLOW_MODEL_URI)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    PULocationID = ride.get('PULocationID')
    DOLocationID = ride.get('DOLocationID')
    trip_distance = ride.get('trip_distance')
    if not (1 <= PULocationID <= 265):
        return jsonify({'error': 'Invalid PULocationID value'}), 400
    if not (1 <= DOLocationID <= 265):
        return jsonify({'error': 'Invalid DOLocationID value'}), 400
    if  not (0 < trip_distance <= 100):
        return jsonify({'error': 'Invalid trip_distance value'}), 400

    try:
        preds = model.predict(ride)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    duration = float(preds[0])
    result = {
        'duration': duration,
        'model_version': MLFLOW_MODEL_VERSION
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)

    # debugging with VSCode
    # app.run(debug=False, host='0.0.0.0', port=4000)
