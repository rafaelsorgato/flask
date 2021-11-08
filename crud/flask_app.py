import flask
import mysql.connector
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import cgi
from base import sql
from flask_login import LoginManager,login_user


app = Flask(__name__)
contaatual=""
senhaatual=""
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'



# URL: localhost:5000
@app.route('/')
def menu():
   return render_template('menu.html')

@app.route('/Contact')
def contact():
   return render_template('Contact.html')



@app.route('/logar' , methods=['GET','POST'])
def logar():
   if request.method == 'POST':
      nome = request.form['name']
      senha = request.form['senha']
      mysql = sql.SQL("root", "123456", "trabalho")
      comando = "SELECT nme_conta,senha_conta,tipo_conta FROM contas WHERE nme_conta = %s and senha_conta = %s"
      cs = mysql.consultar(comando, [nome,senha])
      dados = cs.fetchone()
      cs.close()
      if dados:
         session['logado']=True
         session['senha_conta'] = dados[1]
         session['nme_conta'] = dados[0]
         return render_template('usuario.html')
      if dados == None:
            flash('não existe')
      else:
         flash('erro')
   return flask.render_template('logar.html')



@app.route('/Página-Inicial')
def paginainicial():
      session.pop('logado', None)
      session.pop('senha_conta', None)
      session.pop('nme_conta', None)
      return render_template('Página-Inicial.html')


@app.route('/logout')
def logout():
      session.pop('logado', None)
      session.pop('senha_conta', None)
      session.pop('nme_conta', None)
      # Redirect to login page
      return redirect(url_for('paginainicial'))

@app.route('/registrar',  methods=['GET','POST'])
def registrar():

   if request.method == 'POST':
      form = cgi.FieldStorage()
      nome = request.form['name']
      senha = request.form['senha']
      cpf = request.form['cpf']
      mysql = sql.SQL("root", "123456", "trabalho")
      comando = "SELECT nme_conta,cpf_conta FROM contas WHERE nme_conta = %s or cpf_conta = %s"
      cs = mysql.consultar(comando, [nome,cpf])
      dados = cs.fetchone()
      cs.close()
      if dados == None:
         comando = "insert into contas (nme_conta,cpf_conta,vlr_conta,senha_conta,tipo_conta) values (%s,%s,0,%s,'usuario');"
         if mysql.executar(comando, [nome,cpf,senha]):
            return render_template('sucesso.html')
      elif dados[0] == nome:
         flash("conta já existe, altere o nome")
      elif dados[1] == cpf:
         flash("cpf já está em uso")

   return render_template('registrar.html')


@app.route('/Sobre')
def sobre():
   return render_template('Sobre.html')

@app.route('/usuario')
def usuario():
   if 'logado' in session:
      # User is loggedin show them the home page
      return render_template('usuario.html', username=session['nme_conta'])
   # User is not loggedin redirect to login page
   return redirect(url_for('logar'))




@app.route('/saldo')
def saldo():
   if 'logado' in session:
      mysql = sql.SQL("root", "123456", "trabalho")
      comando = "SELECT vlr_conta FROM contas WHERE nme_conta = %s and senha_conta = %s"
      cs = mysql.consultar(comando, [session['nme_conta'], session['senha_conta']])
      dados = cs.fetchone()
      print(dados)
      cs.close()
      return render_template('saldo.html',username=session['nme_conta'], saldo="saldo= " + str(dados[0]))
      return render_template('saldo.html', )
   # User is not loggedin redirect to login page
   return redirect(url_for('logar'))


app.run(debug=True, use_reloader=False)