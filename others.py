class ConnectError(RuntimeError):
    def __init__(self, error):
        self.error = error