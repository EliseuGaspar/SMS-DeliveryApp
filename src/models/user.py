
class Users:

    def __init__(self, id: int, nome : str, telefone : str, senha : str) -> None:
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.senha = senha
    
    def __repr__(self) -> str:
        return f"usuario <{self.nome}>"
