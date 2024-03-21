class DataNotExist(Exception):
    def __init__(self, message: str = "data not exist"):
        self.message = message
        super().__init__(self.message)


class UserLoginError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
