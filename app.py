from flask import Flask, render_template, jsonify, request

# Import the security checks 
from security.common_passwords import check_common_password
from security.injection import check_injection
from security.compromised_passwords import check_compromised_password

# Create Flask app and display the website
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

# Handle password checks on the website
@app.route("/api/check", methods=["POST"])
def check_password():
    # Get the entered password from the JSON request
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request"}), 400
    
    password = data.get("password")
    
    if not isinstance(password, str) or not password:
        return jsonify({"error": "Password is required"}), 400

    # Run the security checks implemented
    common_result = check_common_password(password)
    injection_result = check_injection(password)
    compromised_result = check_compromised_password(password)

    # Return results to the website
    return jsonify({
        "common_password": common_result,
        "injection_protection": injection_result,
        "compromised_password": compromised_result
    })

# Start the Flask app when the file is run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    