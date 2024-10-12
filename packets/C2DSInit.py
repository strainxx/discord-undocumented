import json
from .BasePacket import Packet

class C2DSInitPacket(Packet):
    def __init__(self) -> None:
        super().__init__()
        self.op = "init"
        self.encoded_public_key: str = None

    def encode(self, encoded_public_key: str) -> str:
        self.encoded_public_key = encoded_public_key
        return json.dumps({
            "op": self.op,
            "encoded_public_key": self.encoded_public_key
        })

    def decode(self, data: dict) -> None:
        self.assert_op(data["op"])
        self.timeout_ms = data["timeout_ms"]
        self.heartbeat_interval = data["heartbeat_interval"]