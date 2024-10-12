from .BasePacket import Packet

class C2DSHeartbeatPacket(Packet):
    def __init__(self) -> None:
        super().__init__()
        self.op = "heartbeat"

    def encode(self) -> str:
        return '{"op": "heartbeat"}'

    def decode(self, data: dict) -> None:
        ...