from .BasePacket import Packet

class DS2CPendingLoginPacket(Packet):
    def __init__(self) -> None:
        super().__init__()
        self.op = "pending_login"
        self.ticket: str = ""

    def encode(self) -> str:
        ...

    def decode(self, data: dict) -> None:
        self.assert_op(data["op"])
        self.ticket = data["ticket"]