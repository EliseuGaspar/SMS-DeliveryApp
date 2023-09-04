from datetime import datetime as dt

class Logs:

    def __init__(self, classe: str, methodname : str, mensagem : str) -> None:
        self.classe = classe
        self.methodname = methodname
        self.mensagem = mensagem
        self.tempo = str(dt.now())
    
    def __repr__(self) -> str:
        return f"classe <{self.classe}>"