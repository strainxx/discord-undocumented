from .BasePacket import Packet

class DS2CHelloPacket(Packet):
    def __init__(self) -> None:
        super().__init__()
        self.op = "hello"
        self.timeout_ms: int = None
        self.heartbeat_interval: int = None

    def encode(self) -> str:
        pass

    def decode(self, data: dict) -> None:
        self.assert_op(data["op"])
        self.timeout_ms = data["timeout_ms"]
        self.heartbeat_interval = data["heartbeat_interval"]