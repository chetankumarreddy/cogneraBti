import re
from typing import Dict, Any

class Chainprint:
    def validate(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        txn_hash = str(txn.get("txn_hash", ""))
        hash_valid = bool(re.match(r"^0x[a-fA-F0-9]{64}$", txn_hash)) and bool(txn.get("hash_valid", True))
        signature_valid = bool(txn.get("signature_valid", True))
        return {
            "hash_valid": hash_valid,
            "signature_valid": signature_valid,
            "cryptographic_assurance": "passed" if hash_valid and signature_valid else "failed",
            "tamper_detected": not hash_valid or not signature_valid,
            "evidence": ["txn_hash", "signature_valid", "hash_valid"]
        }

    def decode(self, txn: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "decoded_function": txn.get("function"),
            "business_action": {
                "mint": "Token deposit minted into Digital Passbook",
                "burn": "Token withdrawal burned from Digital Passbook",
                "transfer": "Token transfer between wallets",
                "fundEscrow": "Escrow contract funded",
                "releaseEscrow": "Escrow released after oracle event"
            }.get(txn.get("function"), "Unrecognised blockchain action"),
            "contract": txn.get("contract_name"),
            "amount": txn.get("amount"),
            "currency": txn.get("currency")
        }
