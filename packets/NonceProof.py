import json
from .BasePacket import Packet

class NonceProofPacket(Packet):
    def __init__(self) -> None:
        super().__init__()
        self.op = "nonce_proof"
        self.encrypted_nonce: str = ""
        self.proof: str = ""

    def encode(self) -> str:
        return json.dumps({
            "op": self.op,
            "proof": self.proof
        })

    def decode(self, data: dict) -> None:
        self.assert_op(data["op"])
        self.encrypted_nonce = data["encrypted_nonce"]