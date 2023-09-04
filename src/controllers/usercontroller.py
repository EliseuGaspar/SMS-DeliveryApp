from ..models.user import Users
from ..models.logs import Logs
from .logscontroller import LogsController
from datetime import datetime as dt
import sqlite3 as sql, logging as log

class UserController():

    def cadastrar_usuario(self, usuario : Users):
        self.conexao()
        try:
            self.cursor.execute(F'''INSERT INTO usuario(id,nome,telefone,senha) VALUES({usuario.id},"{usuario.nome}","{usuario.telefone}","{usuario.senha}")''')
            self.conexao_.commit()
            self.conexao_.close()
            return True
        except Exception as e:
            log.basicConfig(level=log.INFO, filename="src/logs/db/logs.log", format="%(asctime)s - %(levelname)s - %(message)s")
            log.warning(f'[{str(dt.now())[:16]}] => {e}')
    
    def atualizar_usuario(self, usuario : Users):
        self.conexao()
        try:
            self.cursor.execute(F'''UPDATE usuario SET nome = "{usuario.nome}" , telefone = "{usuario.telefone}" , senha = "{usuario.senha}";''')
            self.conexao_.commit()
            self.conexao_.close()
            return True
        except Exception as e:
            log.basicConfig(level=log.INFO, filename="src/logs/db/logs.log", format="%(asctime)s - %(levelname)s - %(message)s")
            log.warning(f'[{str(dt.now())[:16]}] => {e}')
    
    def apagar_usuario(self):
        self.conexao()
        try:
            self.cursor.execute(F'''DELETE FROM usuario WHERE id = {self.pegar_usuario()[0]};''')
            self.conexao_.commit()
            self.conexao_.close()
            return True
        except Exception as e:
            log.basicConfig(level=log.INFO, filename="src/logs/db/logs.log", format="%(asctime)s - %(levelname)s - %(message)s")
            log.warning(f'[{str(dt.now())[:16]}] => {e}')
    
    def pegar_usuario(self):
        self.conexao()
        try:
            try: dados = self.cursor.execute(F'''SELECT * FROM usuario;''').fetchall()[0]
            except: dados = self.cursor.execute(F'''SELECT * FROM usuario;''').fetchall()
            self.conexao_.close()
            return dados
        except Exception as e:
            log.basicConfig(level=log.INFO, filename="src/logs/db/logs.log", format="%(asctime)s - %(levelname)s - %(message)s")
            log.warning(f'[{str(dt.now())[:16]}] => {e}')
    
    def conexao(self):
        try:
            self.conexao_ = sql.connect('src/database/database.db')
            self.cursor = self.conexao_.cursor()
            return True
        except Exception as e:
            log.basicConfig(level=log.INFO, filename="src/logs/db/logs.log", format="%(asctime)s - %(levelname)s - %(message)s")
            log.warning(f'[{str(dt.now())[:16]}] => {e}')