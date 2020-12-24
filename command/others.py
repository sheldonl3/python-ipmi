class ConnectError(RuntimeError):
    def __init__(self, error):
        self.error = error

class Session():
    def __init__(self):
        self.conselon_id = 0
        self.bmc_id=0
        self.cipher_id=0
        self.rand_bmc=0
        self.rand_console=0
        self.sct_bmc=0
        self.sct_console=0
        self.k_bmc=''
        self.k_console=''