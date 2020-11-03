class ConnectError(RuntimeError):
    def __init__(self, error):
        self.error = error

class Session():
    def __init__(self):
        self.conselonid = 0
        self.bmcid=0
        self.cipherid=0

session=Session()