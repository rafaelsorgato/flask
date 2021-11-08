import mysql.connector
from flask import Flask, render_template, request, flash
import cgi

import crud.crudcurso
from crud.crudcurso import *
from flask_login import LoginManager,login_user


class SQL:
   def __init__(self, usuario, senha, esquema):
       self.cnx = mysql.connector.connect(user=usuario, password=senha,\
                                          host='127.0.0.1',\
                                          database=esquema)

   def executar(self, comando, parametros):
       cursor = self.cnx.cursor()
       cursor.execute(comando, parametros)
       self.cnx.commit()
       cursor.close()
       return True

   def consultar(self, comando, parametros):
       cursor = self.cnx.cursor()
       cursor.execute(comando, parametros)
       return cursor

   def __del__(self):
       self.cnx.close()



class user:

   def __init__(self,nome,senha):
        self.nomes=nome
        self.senhas=senha

   @property
   def is_authenticated(self):
       return True

   @property
   def is_active(self):
       return True

   @property
   def is_anonymous(self):
       return False

   @property
   def get_id(self):
       return str(self.id)

