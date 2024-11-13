from web3 import Web3


def generate_certificate_hash(name, course, grade):
    # Use Web3.solidityKeccak to match Solidity's keccak256(abi.encodePacked(...))
    cert_hash = Web3.solidity_keccak(
        ['string', 'string', 'string'],
        [name, course, grade]
    )
    return '0x' + cert_hash.hex()  # Convert to hex format with '0x' prefix

# Example usage
name = "A"
course = "A"
grade = "A"

hash_result = generate_certificate_hash(name, course, grade)
print("Certificate Hash:", hash_result)
