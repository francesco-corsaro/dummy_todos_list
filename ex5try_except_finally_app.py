# Questo file utilizza il metodo fetch e implementa try-except-finally
# quindi l'applicazione diventa asincrona e verrà
# implementato codice javascript sul file index 
from flask import Flask,render_template, request, redirect, url_for, jsonify, abort
# aggiungiamo la libreria abort per gestire gli errori

import sys # un'altra libreria per gestire gli errori

from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)  # crea un'aplicazione che prende il  nome del nostro file
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://fra3@localhost:5432/eg_sql_alchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<Person ID: {}, description: {}>".format(self.id,self.description)

db.create_all() 

@app.route('/todos/create', methods=['POST'])

# poi creiamo un handler per gestire quello che succede su /todos/create
def create_todo():
    error= False
    body={}
    try:
        description =  request.get_json()['description'] # questo prende i dati dal client
       
        new_raw = Todo(description= description) # questa è la procedura per inserire i dati nel database
        db.session.add(new_raw)
        db.session.commit()
        
        body['description']= new_raw.description # data la modalità try-except-finally che prevede la chiusura della session
                                                 # assegnamo il valore ad una variabile in questo caso body
    except: #in caso di errore lo gestiamo
        error= True
        db.session.rollback()  # ci permete di evitare che dati in sospeso vengano inseriti
        print(sys.exc_info())
    finally: # nel finally chiudiamo la sessione
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body) # questo è l'oggetto json 


@app.route("/")
def index():
    # qui utiliziamo render_template in modo che gli utenti visulizzino
    # la pagina html (in questo caso) desiderata
    return render_template('index.html', data = Todo.query.all())

if __name__ == '__main__':
    app.run()
