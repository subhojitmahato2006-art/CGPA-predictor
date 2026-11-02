import os

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No input data received."}), 400

    cgpas = data.get("cgpas")
    trend = data.get("trend", 0)

    if not isinstance(cgpas, list) or not cgpas:
        return jsonify({
            "error": "Enter at least one semester CGPA."
        }), 400

    try:
        cgpas = [float(value) for value in cgpas]
        trend = float(trend)
    except (TypeError, ValueError):
        return jsonify({"error": "Enter valid numeric values."}), 400

    if any(not 0 <= value <= 10 for value in cgpas):
        return jsonify({
            "error": "Every CGPA must be between 0 and 10."
        }), 400

    if trend not in (-1, -0.5, 0, 0.5, 1):
        return jsonify({"error": "Invalid performance trend."}), 400

    average = sum(cgpas) / len(cgpas)
    predicted_cgpa = max(0, min(10, average + trend))

    if predicted_cgpa > average:
        message = "Your selected trend predicts an improvement."
    elif predicted_cgpa < average:
        message = "Your selected trend predicts a decrease."
    else:
        message = "Your prediction assumes similar performance."

    return jsonify({
        "average": round(average, 2),
        "predicted_cgpa": round(predicted_cgpa, 2),
        "message": message
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
