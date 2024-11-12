// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateRegistry {
    struct Certificate {
        bytes32 hash;
        bool isRevoked;
    }

    address public owner;
    mapping(address => bool) public authorizedIssuers; // Mapping to store authorized issuer addresses
    mapping(bytes32 => Certificate) public certificates;

    event CertificateIssued(bytes32 indexed hash, string studentID);
    event CertificateRevoked(bytes32 indexed hash, string studentID);
    event IssuerAdded(address indexed issuer);
    event IssuerRemoved(address indexed issuer);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    modifier onlyAuthorizedIssuer() {
        require(authorizedIssuers[msg.sender], "Not an authorized issuer");
        _;
    }

    constructor() {
        owner = msg.sender; // Set the contract deployer as the owner
    }

    // Function for the owner to add a new authorized issuer
    function addIssuer(address _issuer) public onlyOwner {
        authorizedIssuers[_issuer] = true;
        emit IssuerAdded(_issuer);
    }

    // Function for the owner to remove an authorized issuer
    function removeIssuer(address _issuer) public onlyOwner {
        authorizedIssuers[_issuer] = false;
        emit IssuerRemoved(_issuer);
    }

    // Function to issue a certificate, restricted to authorized issuers
    function issueCertificate(
        string memory name,
        string memory course,
        string memory studentID,
        string memory teacherName,
        string memory grade,
        uint marks,
        string memory issueDate
    ) public onlyAuthorizedIssuer {
        bytes32 certHash = keccak256(
            abi.encodePacked(name, course, studentID, teacherName, grade, marks, issueDate)
        );

        require(certificates[certHash].hash == 0, "Certificate already exists.");
        
        certificates[certHash] = Certificate(certHash, false); // Store the hash and mark as not revoked
        emit CertificateIssued(certHash, studentID);
    }

    // Function to revoke a certificate, restricted to authorized issuers
    function revokeCertificate(
        string memory name,
        string memory course,
        string memory studentID,
        string memory teacherName,
        string memory grade,
        uint marks,
        string memory issueDate
    ) public onlyAuthorizedIssuer {
        bytes32 certHash = keccak256(
            abi.encodePacked(name, course, studentID, teacherName, grade, marks, issueDate)
        );

        require(certificates[certHash].hash != 0, "Certificate does not exist.");
        require(!certificates[certHash].isRevoked, "Certificate already revoked.");

        certificates[certHash].isRevoked = true;
        emit CertificateRevoked(certHash, studentID);
    }

    // Function to verify if a certificate is valid, revoked, or does not exist
    function verifyCertificate(
        string memory name,
        string memory course,
        string memory studentID,
        string memory teacherName,
        string memory grade,
        uint marks,
        string memory issueDate
    ) public view returns (string memory) {
        bytes32 certHash = keccak256(
            abi.encodePacked(name, course, studentID, teacherName, grade, marks, issueDate)
        );

        if (certificates[certHash].hash == 0) {
            return "Certificate does not exist.";
        } else if (certificates[certHash].isRevoked) {
            return "Certificate is revoked.";
        } else {
            return "Certificate is valid.";
        }
    }
}
