from py_ecc.bls import G2ProofOfPossession as bls
from py_ecc.bls.g2_primitives import pubkey_to_G1
from py_ecc.optimized_bls12_381 import curve_order
import secrets
import hashlib

class Client:
    def __init__(self, id):
        self.id = id
        # Generate a valid BLS private key as an integer
        while True:
            self.private_key = secrets.randbits(256)
            if 0 < self.private_key < curve_order:
                break
        self.public_key = bls.SkToPk(self.private_key)
    
    def sign_message(self, message):
        message_hash = hashlib.sha256(message.encode()).digest()
        return bls.Sign(self.private_key, message_hash)
    
    def get_public_key_g1(self):
        return pubkey_to_G1(self.public_key)

class Verifier:
    @staticmethod
    def verify_individual_signature(client, message, signature):
        message_hash = hashlib.sha256(message.encode()).digest()
        return bls.Verify(client.public_key, message_hash, signature)
    
    @staticmethod
    def verify_aggregated_signature(public_keys, message, aggregated_signature):
        message_hash = hashlib.sha256(message.encode()).digest()
        return bls.AggregateVerify([(pk, message_hash) for pk in public_keys], aggregated_signature)

def main():
    num_clients = 3
    clients = [Client(i) for i in range(num_clients)]
    message = "Test message for BLS signatures"

    print("=== Individual Signatures ===")
    signatures = []
    for client in clients:
        signature = client.sign_message(message)
        signatures.append(signature)
        is_valid = Verifier.verify_individual_signature(client, message, signature)
        print(f"Client {client.id} signature valid: {is_valid}")

    print("\n=== Aggregated Signature ===")
    aggregated_sig = bls.Aggregate(signatures)
    public_keys = [client.public_key for client in clients]
    is_valid = Verifier.verify_aggregated_signature(public_keys, message, aggregated_sig)
    print(f"Aggregated signature valid: {is_valid}")

if __name__ == "__main__":
    main()
