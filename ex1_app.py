from flask import Flask,render_template  
# usiamo la libreria render_template ^   
# questa libreria ci permette divisualizzare
# file html, xml xhml
# 
app= Flask(__name__)  # crea un'aplicazione che prende il  nome del nostro file

@app.route("/")

def index():
    # qui utiliziamo render_template in momdo che gli utenti visulizzino
    # la pagina html (in questo caso) desiderata
    return render_template('index.html', data=[{
        'description' : 'Todo1'
    },{
        'description' : 'Todo2'
    },{
        'description' : 'Todo3'
    },{
        'description' : 'Todo4'
    },{
        'description' : 'Todo5'
    }])