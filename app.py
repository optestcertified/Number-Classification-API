from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Check if a number is prime (only valid for integers)
def is_prime(n):
    if n < 2 or not n.is_integer():
        return False
    n = int(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Check if a number is perfect (only valid for positive integers)
def is_perfect(n):
    if n < 2 or not n.is_integer():
        return False
    n = int(n)
    return sum(i for i in range(1, n) if n % i == 0) == n

# Check if a number is an Armstrong number (only valid for integers)
def is_armstrong(n):
    if not n.is_integer():
        return False
    num_str = str(int(n))
    num_digits = len(num_str)
    return sum(int(digit) ** num_digits for digit in num_str) == int(n)

# Check parity (even/odd, only for integers)
def get_parity(n):
    return "even" if n.is_integer() and int(n) % 2 == 0 else "odd"

# Calculate digit sum (only for integers)
def digit_sum(n):
    if not n.is_integer():
        return None  # Digit sum is undefined for floating-point numbers
    return sum(int(digit) for digit in str(abs(int(n))))  # Handle negatives properly

# Fetch a fun fact about the number
def get_fun_fact(n):
    if not n.is_integer():
        return "Fun facts are only available for whole numbers."
    url = f"http://numbersapi.com/{int(n)}/math"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException:
        return "Fun fact unavailable at the moment."
    return f"No fun fact available for {n}."

# Get all properties of a number
def get_properties(n):
    properties = [get_parity(n)]
    if is_armstrong(n):
        properties.append("armstrong")
    return properties

# API Endpoint
@app.route("/api/classify-number", methods=['GET'])
def classify_number():
    number_str = request.args.get("number")

    # Validate input: Ensure it's a valid number (integer or float)
    try:
        number = float(number_str)
    except (TypeError, ValueError):
        return jsonify({"number": "alphabet", "error": True}), 400

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": get_properties(number),
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number),
    }

    # Override fun fact if Armstrong number
    if is_armstrong(number):
        digits = [int(d) for d in str(int(number))]
        length = len(digits)
        calculation = " + ".join(f"{d}^{length}" for d in digits) + f" = {int(number)}"
        response["fun_fact"] = f"{int(number)} is an Armstrong number because {calculation}"

    return jsonify(response), 200  # Ensuring all valid numbers return 200

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


