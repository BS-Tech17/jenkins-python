from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Jenkins Pipeline works!"

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8081))
    app.run(host="0.0.0.0", port=8081, debug=False, threaded=True)
