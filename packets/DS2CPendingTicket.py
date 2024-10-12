import base64
from .BasePacket import Packet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

class DS2CPendingTicketPacket(Packet):
    def __init__(self) -> None:
        super().__init__()
        self.op = "pending_ticket"
        self.snowflake: int = 0
        self.discriminator: int = 0
        self.avatar_hash: str = ""
        self.username: str = ""

    def encode(self) -> str:
        ...

    def decode(self, data: dict, private_key) -> None:
        self.assert_op(data["op"])
        encr = data["encrypted_user_payload"]

        decrypted_nonce = private_key.decrypt(
            base64.b64decode(encr),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # print()
        ddata = decrypted_nonce.decode().split(":")

        self.snowflake = int(ddata[0])
        self.discriminator = int(ddata[1])
        self.avatar_hash = ddata[2]
        self.username = ddata[3]
