import colorama
import dsapi

token = ""

qrlink = input("Enter link from qr code: ")

fingerprint = qrlink.split("/ra/")[1]

print("Fingerprint", fingerprint)

discord = dsapi.RemoteAuth(token)

discord.remote_auth_init(fingerprint)

discord.remote_auth_finish()