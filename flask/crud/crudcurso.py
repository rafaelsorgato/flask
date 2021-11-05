import mysql.connector
from flask import Flask, render_template, request
import cgi
from base import sql
app = Flask(__name__)
contaatual=""
senhaatual=""

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
      comando = "SELECT conta,senha,tipo FROM contas WHERE conta = %s and senha = %s"
      cs = mysql.consultar(comando, [nome,senha])
      dados = cs.fetchone()
      cs.close()
      if dados == None:
            return 'não existe'
      elif dados[0]==nome and dados[1]==senha:
         global contaatual
         global senhaatual
         contaatual=dados[0]
         senhaatual=dados[1]
         print(contaatual)
         print(senhaatual)
         if dados[2]=="usuario":
            return render_template('usuario.html')
         elif dados[2]=="funcionario":
            return "funcionario"
      else:
         return 'erro'
   return render_template('logar.html')

@app.route('/Página-Inicial')
def paginainicial():
      return render_template('menu.html')

@app.route('/registrar',  methods=['GET','POST'])
def registrar():
   if request.method == 'POST':
      form = cgi.FieldStorage()
      nome = request.form['name']
      senha = request.form['senha']
      mysql = sql.SQL("root", "123456", "trabalho")
      comando = "SELECT conta FROM contas WHERE conta = %s"
      cs = mysql.consultar(comando, [nome])
      dados = cs.fetchone()
      cs.close()
      if dados == None:
         comando = "insert into contas (conta,senha,tipo,saldo) values (%s,%s,'usuario',0);"
         if mysql.executar(comando, [nome,senha]):
            return render_template('sucesso.html')
      elif dados[0] == nome:
         return 'CONTA JA ESTA EM USO'

   return render_template('registrar.html')


@app.route('/Sobre')
def sobre():
   return render_template('Sobre.html')

@app.route('/usuario')
def usuario():
   print(contaatual)
   print(senhaatual)
   return render_template('usuario.html')

@app.route('/saldo')
def saldo():
   mysql = sql.SQL("root", "123456", "trabalho")
   comando = "SELECT saldo FROM contas WHERE conta = %s and senha = %s"
   cs = mysql.consultar(comando, [contaatual, senhaatual])
   dados = cs.fetchone()
   print(contaatual)
   print(senhaatual)
   print(dados)
   cs.close()
   return render_template('saldo.html', saldo="saldo= "+str(dados[0]))


app.run(debug=True, use_reloader=False)