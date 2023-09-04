from ..models.logs import Logs


class LogsController:

    def __init__(self) -> None:
        self.db_path = 'src/logs/db/logs.log'
        self.acesso_path = 'src/logs/acesso/logs.log'
        self.conta_path = 'src/logs/conta/logs.log'

    def writelog(self, log : Logs, type : str) -> None:
        self.log = log
        if type == 'db':
            self.__write__(self.db_path)
        elif type == 'acesso':
            self.__write__(self.acesso_path)
        elif type == 'conta':
            self.__write__(self.conta_path)
    
    def __write__(self, path : str) -> None:
        with open(file=path,mode='a+') as file:
            file.write(F"""\n[{self.log.classe}({self.log.methodname}) -> {self.log.tempo}] {self.log.mensagem}""")