from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/check", methods=["POST"])
def check_password():
    # Placeholder results for now
    return jsonify({
        "common_password": "Not implemented",
        "injection_protection": "Not implemented",
        "compromised_password": "Not implemented"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
