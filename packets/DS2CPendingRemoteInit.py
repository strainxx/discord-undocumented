from .BasePacket import Packet

class DS2CPendingRemoteInitPacket(Packet):
    def __init__(self) -> None:
        super().__init__()
        self.op = "pending_remote_init"
        self.fingerprint: str = ""

    def encode(self) -> str:
        ...

    def decode(self, data: dict) -> None:
        self.assert_op(data["op"])
        self.fingerprint = data["fingerprint"]