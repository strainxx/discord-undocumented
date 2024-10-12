import requests

class RemoteAuth:
    def __init__(self, token: str = None) -> None:
        self.api = "https://discord.com/api/v9/users/@me/remote-auth/"
        self.token = token
        self.session = requests.Session()

        self.handshake_token: str = ""

        if token != None:
            self.session.headers.update({
                "Authorization": token
            })

    def login(self, ticket: str):
        endpoint = self.api+"login"

        r = self.session.post(endpoint, json={
            "ticket": ticket
        })

        return r.json()["encrypted_token"]
    
    def remote_auth_init(self, fingerprint: str):
        endpoint = self.api[:-1]

        r = self.session.post(endpoint, json={
            "fingerprint": fingerprint
        })

        print(r.json())
        self.handshake_token = r.json()["handshake_token"]

    def remote_auth_finish(self):
        endpoint = self.api + "finish"

        r = self.session.post(endpoint, json={
            "handshake_token": self.handshake_token,
            "temporary_token": False
        })

class User:
    def __init__(self, token: str) -> None:
        self.api = "https://discord.com/api/v9/users/@me/"
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": token
        })

    def get_relationships(self):
        endpoint = self.api+"relationships"

        return self.session.get(endpoint).text
    
    def create_friend_invite(self):
        endpoint = self.api+"invites"

        return self.session.post(endpoint).json()