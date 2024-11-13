import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from sepolia import (decode_input_data, generate_certificate_hash,
                     get_transaction_details_etherscan,
                     get_transactions_etherscan, issue_certificate,
                     revoke_certificate, verify_certificate)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["DEBUG"] = True

contract_address = "0xD75A3eeD94e27C40EB99C38d786E16DCD7D563d0"


@app.route("/issue", methods=["POST"])
def issue():
    data = json.loads(request.data)
    details = data["details"]
    from_address = "0xC612891924e292e5214Da3A227AA8CC9274849ef"
    with open("meta.key", "r") as f:
        private_key = f.read().strip()
    #     private_key,
    # private_key = data["private_key"]
    # from_address = data["from_address"]
    hash = issue_certificate(details, from_address, private_key)
    return jsonify({"tx_hash": hash})


@app.route("/get_transactions", methods=["GET"])
def get_transactions():
    address = "0xD75A3eeD94e27C40EB99C38d786E16DCD7D563d0"
    transactions = get_transactions_etherscan(address)
    return jsonify(transactions)


@app.route("/revoke", methods=["POST"])
def revoke():
    name = request.args.get("name")
    course = request.args.get("course")
    grade = request.args.get("grade")
    from_address = "0xC612891924e292e5214Da3A227AA8CC9274849ef"
    with open("meta.key", "r") as f:
        private_key = f.read().strip()
    tx_hash = generate_certificate_hash(name, course, grade)
    result = {"result": revoke_certificate(tx_hash,from_address,private_key)}

    return jsonify(result)
@app.route("/verify", methods=["GET"])
def verify():
    try:
        name = request.args.get("name")
        course = request.args.get("course")
        grade = request.args.get("grade")
        tx_hash = generate_certificate_hash(name, course, grade)
        result = {"result": verify_certificate(tx_hash)}
        # result["etherscan"] = get_transaction_details_etherscan(tx_hash)

        return jsonify(result)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 404)


@app.route("/issued_certificates", methods=["GET"])
def get_issued_certificates():
    address = "0xC612891924e292e5214Da3A227AA8CC9274849ef"
    transactions = get_transactions_etherscan(address)
    certificates = []
    for tx in transactions:
        _, params = decode_input_data(tx)
        if params:
            params["tx_hash"] = tx
            cert_hash = generate_certificate_hash(
                params["name"], params["course"], params["grade"]
            )
            params["cert_hash"] = cert_hash
            certificates.append(params)
    return jsonify(certificates)


def main():
    app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
