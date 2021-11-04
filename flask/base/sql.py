from flask import Flask, render_template, request
import cgi
app = Flask(__name__)

@app.route('/')
def receber():
   return render_template('Página-Inicial.html')


@app.route('/static/logar.html',  methods=['POST','GET'])
def recebera():
    print('rafa')
    form = cgi.FieldStorage()
    nome = form.getvalue('name')
    senha = form.getvalue('message')
    print(nome)
    print(senha)
    return render_template('logar.html')

@app.route('/static/registrar.html', methods=['POST'])
def receberas():
    print('rafa')
    return render_template('registrar.html')


@app.route('/operacoes', methods=['POST'])
def operacoes():
    texto=''
    a=int(request.form['primeiro'])
    b=int(request.form['primeiro'])
    texto+='<li>' + 'soma=' + str(a+b) + '</li>\n'
    texto+='<li>' + 'subtração='+ str(a-b) + '</li>\n'
    texto+='<li>' + 'multiplicação='+ str(a*b) + '</li>\n'
    texto+='<li>' + 'divisão='+ str(a/b) + '</li>\n'

    return render_template('operacoes.html', t_operacoes=texto)

@app.route('/contar', methods=['POST'])
def contar():
   contagem = ''
   for c in range(0, 2001, 2):
       contagem += '<li>' + str(c) + '</li>\n'

   return render_template('contar.html', t_ni=0, t_nf=2000, t_p=2, t_contagem=contagem)


app.debug=1
app.run()
