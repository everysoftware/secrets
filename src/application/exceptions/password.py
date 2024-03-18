class ServerPasswordNotFound(ValueError):
    def __init__(self, ident: int):
        super().__init__(f"Password {ident} not found")
        self.ident = ident
