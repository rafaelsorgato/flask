from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/escolher')
def receber():
   return render_template('escolher.html')

@app.route('/fibonacci', methods=['POST'])
def fibonacci():
    vetor=[]
    texto=''
    anterior = 0
    proximo = 0
    x=0
    while (proximo < 30):
        texto+= '<li>' + str(proximo) + '</li>\n'
        vetor[x]= texto
        x+=1
        proximo = proximo + anterior
        anterior = proximo - anterior
        if (proximo == 0):
            proximo = proximo + 1
    return str(vetor(int(request.args['n'])))

@app.route('/contar', methods=['POST'])
def contar():
   contagem = ''
   for c in range(0, 2001, 2):
       contagem += '<li>' + str(c) + '</li>\n'

   return render_template('contar.html', t_ni=0, t_nf=2000, t_p=2, t_contagem=contagem)


app.debug=1
app.run()
