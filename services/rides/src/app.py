import os

from flask import Flask, request, jsonify
import mlflow


MLFLOW_MODEL_URI = os.getenv('MLFLOW_MODEL_URI', None)
assert MLFLOW_MODEL_URI is not None, "Missing MLFLOW_MODEL_URI"

MLFLOW_MODEL_VERSION = os.getenv('MLFLOW_MODEL_VERSION', None)


app = Flask('duration-prediction')
model = mlflow.pyfunc.load_model(MLFLOW_MODEL_URI)


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    preds = model.predict(ride)
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
