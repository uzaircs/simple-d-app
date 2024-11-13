from eth_abi import encode
from eth_hash.auto import keccak
from web3 import Web3

# Connect to Sepolia via Infura
infura_url = "https://sepolia.infura.io/v3/74849d62f4454b0dbf7622b8eb6e43d9"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract address and ABI
contract_address = "0xD75A3eeD94e27C40EB99C38d786E16DCD7D563d0"
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_issuer",
				"type": "address"
			}
		],
		"name": "addIssuer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "hash",
				"type": "bytes32"
			}
		],
		"name": "CertificateIssued",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "hash",
				"type": "bytes32"
			}
		],
		"name": "CertificateRevoked",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "course",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "grade",
				"type": "string"
			}
		],
		"name": "issueCertificate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "issuer",
				"type": "address"
			}
		],
		"name": "IssuerAdded",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "issuer",
				"type": "address"
			}
		],
		"name": "IssuerRemoved",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_issuer",
				"type": "address"
			}
		],
		"name": "removeIssuer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "certHash",
				"type": "bytes32"
			}
		],
		"name": "revokeCertificate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "authorizedIssuers",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "certificateHashes",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "certificates",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "hash",
				"type": "bytes32"
			},
			{
				"internalType": "bool",
				"name": "isRevoked",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAllCertificateHashes",
		"outputs": [
			{
				"internalType": "bytes32[]",
				"name": "",
				"type": "bytes32[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "certHash",
				"type": "bytes32"
			}
		],
		"name": "verifyCertificate",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)


# Function to issue a certificate
def issue_certificate(details, from_address, private_key):
    tx = contract.functions.issueCertificate(
        details["name"],
        details["course"],
        details["grade"],
       
    ).build_transaction(
        {
            "from": from_address,
            "gas": 200000,
            "nonce": web3.eth.get_transaction_count(from_address),
        }
    )

    # Sign and send transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return web3.to_hex(tx_hash)


private_key = None
with open("meta.key", "r") as f:
    private_key = f.read().strip()
# Issue a certificate
# issue_certificate(
#     {
#         "name": "Alice",
#         "course": "Blockchain 101",
#         "studentID": "S12345",
#         "teacherName": "Dr. John",
#         "grade": "A",
#         "marks": 95,
#         "issueDate": "2023-11-15",
#     },
#     "0xC612891924e292e5214Da3A227AA8CC9274849ef",
#     private_key,
# )
import requests


def decode_input_data(tx_hash):
    try:
        tx = web3.eth.get_transaction(tx_hash)
        input_data = tx["input"]
        if tx["to"] != contract_address:
            return None, None
        input_data = tx["input"]
        decoded_function, decoded_params = contract.decode_function_input(input_data)
        return decoded_function.fn_name, decoded_params
    except Exception as e:
        print("An error occurred:", e)


def get_transaction_details_etherscan(tx_hash):
    api_key = "BEKCAMQZS5JJHQ9CP11XMC3CW9K64C5P23"
    url = f"https://api-sepolia.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={tx_hash}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    if "result" in data:
        receipt = data["result"]
        status = receipt.get("status")
        if status == "0x1":
            return "Success"
        elif status == "0x0":
            return "Failure"
        else:
            return "Unknown status"
    else:
        print("Error retrieving transaction receipt:", data.get("message"))
        return None


def generate_certificate_hash(name, course, grade):
    # Use Web3.solidityKeccak to match Solidity's keccak256(abi.encodePacked(...))
    cert_hash = Web3.solidity_keccak(
        ['string', 'string', 'string'],
        [name, course, grade]
    )
    return '0x' + cert_hash.hex()  # Convert to hex format with '0x' prefix


def get_transactions_etherscan(address):
    api_key = "BEKCAMQZS5JJHQ9CP11XMC3CW9K64C5P23"
    url = f"https://api-sepolia.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}"

    response = requests.get(url)
    hashes = []
    for tx in response.json()["result"]:
        if tx["input"].startswith("0xbeec1caa"):
            hashes.append(tx["hash"])
    data = response.json()

    if data["status"] == "1":  # Status '1' means success
        return hashes


if __name__ == "main":
    transactions = get_transactions_etherscan(contract_address)
    for tx in transactions:
        _, params = decode_input_data(tx)
        if params:
            print(params)
            print(
                f'Certificate issued to {params["studentID"]} on {params["issueDate"]} to {params["name"]} for {params["course"]} by {params["teacherName"]} with grade {params["grade"]} and marks {params["marks"]}'
            )


def verify_certificate(tx_hash):
    return contract.functions.verifyCertificate(tx_hash).call()


def revoke_certificate(tx_hash, from_address, private_key):

    tx = contract.functions.revokeCertificate(tx_hash).build_transaction(
        {
            "from": from_address,
            "gas": 200000,
            "nonce": web3.eth.get_transaction_count(from_address),
        }
    )

    # Sign and send transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return web3.to_hex(tx_hash)
