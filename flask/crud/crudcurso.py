import mysql.connector
import locale
from base import bd
from flask import Flask, render_template, request
from . import criarcurso

app = Flask(__name__)

# URL: localhost:5000
@app.route('/')
def menu():
   return render_template('menu.html')

# URL: localhost:5000/formincluir
@app.route('/formincluir')
def formIncluir():
   return render_template('formincluir.html')

@app.route('/incluir', methods=['POST'])
def incluir():
   # Recuperando dados do formulário de formIncluir()
   nome = request.form['nome']
   sigla = request.form['sigla']
   data = request.form['data']
   creditos = float(request.form['creditos'])
   ementa = request.form['ementa']

   # Incluindo dados no SGBD
   mysql = bd.SQL("root", "123456", "tarefaatual")
   comando = "INSERT INTO tb_curso(nme_curso, sigla_curso, dta_curso, num_creditos, ementa) VALUES (%s, %s, %s, %s, %s);"
   if mysql.executar(comando, [nome, sigla, data, creditos, ementa]):
       msg="curso " + nome + " cadastrado com sucesso!"
   else:
       msg="Falha na inclusão do curso."

   return render_template('incluir.html', msg=msg)


@app.route('/parconsultar')
def parConsultar():
   # Recuperando modelos existentes na base de dados
   mysql = bd.SQL("root", "123456", "tarefaatual")
   comando = "SELECT DISTINCT nme_curso FROM tb_curso ORDER BY nme_curso;"

   cs = mysql.consultar(comando, ())
   sel = "<SELECT NAME='modelo'>"
   sel += "<OPTION>Todos</OPTION>"
   for [modelo] in cs:
       sel += "<OPTION>" + modelo + "</OPTION>"
   sel += "</SELECT>"
   cs.close()

   # Recuperando menor e maior data de curso
   comando="SELECT MIN(dta_curso) AS menor, MAX(dta_curso) AS maior FROM tb_curso;"
   cs = mysql.consultar(comando, ())
   dados = cs.fetchone()
   menor = dados[0]
   maior = dados[1]

   return render_template('parconsultar.html', modelo=sel, menor=menor, maior=maior)


@app.route('/consultar', methods=['POST'])
def consultar():
   # Pegando os dados de parâmetro vindos do formulário parConsultar()
   curso = request.form['modelo']
   menor = request.form['ini']
   maior = request.form['fim']

   # Testando se é para considerar todos os modelos
   curso = "" if curso=="Todos" else curso

   # Recuperando modelos que satisfazem aos parâmetros de filtragem
   mysql = bd.SQL("root", "123456", "tarefaatual")
   comando = "SELECT * FROM tb_curso WHERE nme_curso LIKE CONCAT('%', %s, '%') AND dta_curso BETWEEN %s AND %s ORDER BY dta_curso;"

   locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')

   cs = mysql.consultar(comando, [curso, menor, maior])
   cursos = ""
   for [idt, sigla, nome, data, creditos, ementa] in cs:
       cursos += "<TR>"
       cursos += "<TD>" + sigla + "</TD>"
       cursos += "<TD>" + nome + "</TD>"
       cursos += "<TD>" + str(data) + "</TD>"
       cursos += "<TD>" + str(creditos) + "</TD>"
       cursos += "<TD>" + ementa + "</TD>"
       cursos += "</TR>"
   cs.close()

   return render_template('consultar.html', cursos=cursos)


@app.route('/paralterar')
def parAlterar():
   return render_template('paralterar.html')


@app.route('/formalterar', methods=['POST'])
def formAlterar():
   # Pegando os dados de parâmetro vindos do formulário parConsultar()
   nome = request.form['nome']

   # Recuperando modelos que satisfazem aos parâmetros de filtragem
   mysql = bd.SQL("root", "123456", "tarefaatual")
   comando = "SELECT * FROM tb_curso WHERE nme_curso=%s;"

   cs = mysql.consultar(comando, [nome])
   dados = cs.fetchone()
   cs.close()

   if dados == None:
      return render_template('naoencontrado.html')
   else:
      return render_template('formalterar.html', idt=dados[0], sigla=dados[1], nome=dados[2], data=dados[3],
                             creditos=dados[4], ementa=dados[5])


@app.route('/alterar', methods=['POST'])
def alterar():
   # Recuperando dados do formulário de formAlterar()
   idt = int(request.form['idt'])
   sigla = request.form['sigla']
   nome = request.form['nome']
   data = float(request.form['data'])
   creditos = float(request.form['creditos'])
   ementa = request.form['ementa']

   # Alterando dados no SGBD
   mysql = bd.SQL("root", "123456", "tarefaatual")
   comando = "UPDATE tb_curso SET sigla_curso=%s, nme_curso=%s, dta_curso=%s, num_creditos=%s, ementa=%s WHERE idt_curso=%s;"

   if mysql.executar(comando, [sigla, nome, data, creditos, ementa, idt]):
      msg = "curso " + nome + " alterado com sucesso!"
   else:
      msg = "Falha na alteração do curso."

   return render_template('alterar.html', msg=msg)
