import asyncio
import hashlib
import json
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64
from websockets.sync.client import connect
from packets.DS2CHello import DS2CHelloPacket
from packets.C2DSInit import C2DSInitPacket
from packets.C2DSHeartbeat import C2DSHeartbeatPacket
from packets.NonceProof import NonceProofPacket
from packets.DS2CPendingRemoteInit import DS2CPendingRemoteInitPacket
from packets.DS2CPendingTicket import DS2CPendingTicketPacket
from packets.DS2CPendingLogin import DS2CPendingLoginPacket

import dsapi

import colorama

def current_milli_time():
    return round(time.time() * 1000)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

spki_der = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

spki_base64 = base64.b64encode(spki_der).decode('utf-8')
print(colorama.Fore.LIGHTCYAN_EX+"SPKI GENERATED:", spki_base64, colorama.Style.RESET_ALL)

def hello():
    with connect("wss://remote-auth-gateway.discord.gg/?v=2", additional_headers={
        'Origin': 'https://discord.com',
    }) as websocket:
        last_milis = current_milli_time()

        message = websocket.recv()

        # Handshaking
        hello_packet = DS2CHelloPacket()
        hello_packet.decode(json.loads(message))
        print(colorama.Fore.GREEN+f"Hello msg received! hb_interval: {hello_packet.heartbeat_interval}", colorama.Style.RESET_ALL)
        init_packet = C2DSInitPacket()
        i_ = init_packet.encode(spki_base64)
        print("Sending init msg")
        websocket.send(i_)

        while True:
            message = websocket.recv()
            print(f"Received: {message}")
            p = json.loads(message)

            match p["op"]:
                case "nonce_proof":
                    nonce_packet = NonceProofPacket()
                    nonce_packet.decode(p)

                    e_nonce = base64.b64decode(nonce_packet.encrypted_nonce)

                    decrypted_nonce = private_key.decrypt(
                        e_nonce,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )

                    sha256_hash = hashlib.sha256(decrypted_nonce).digest()

                    base64url_encoded_hash = base64.urlsafe_b64encode(sha256_hash).rstrip(b'=').decode('utf-8')


                    print(colorama.Fore.GREEN+f"Decrypted nonce hash! {base64url_encoded_hash}"+colorama.Style.RESET_ALL)

                    nonce_packet.proof = base64url_encoded_hash

                    websocket.send(nonce_packet.encode())

                case "pending_remote_init":
                    pri_packet = DS2CPendingRemoteInitPacket()
                    pri_packet.decode(p)
                    print(colorama.Fore.LIGHTMAGENTA_EX+f"https://discordapp.com/ra/{pri_packet.fingerprint}"+colorama.Style.RESET_ALL)

                case "pending_ticket":
                    pt_packet = DS2CPendingTicketPacket()
                    pt_packet.decode(p, private_key)

                    print(f"Get user: {pt_packet.username}#{pt_packet.discriminator}")

                case "pending_login":
                    pl_packet = DS2CPendingLoginPacket()
                    pl_packet.decode(p)

                    RA_api = dsapi.RemoteAuth()
                    encr_token = RA_api.login(pl_packet.ticket)

                    # print(encr_token)

                    e_token = base64.b64decode(encr_token)

                    decrypted_nonce = private_key.decrypt(
                        e_token,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )

                    print(colorama.Fore.GREEN + "Decoded token: " + decrypted_nonce.decode() + colorama.Style.RESET_ALL)


                case _:
                    print(colorama.Fore.RED+f"Received unknown packet! {p['op']}"+colorama.Style.RESET_ALL)

            if current_milli_time() - last_milis > hello_packet.heartbeat_interval:
                last_milis = current_milli_time()
                hb_packet = C2DSHeartbeatPacket()
                websocket.send(hb_packet.encode())

hello()