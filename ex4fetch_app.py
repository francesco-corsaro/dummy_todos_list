# Questo file utilizza il metodo fetch 
# quindi l'applicazione diventa asincrona e verrà
# implementato codice javascript sul file index 
from flask import Flask,render_template, request, redirect, url_for, jsonify
# aggiungiamo la libreria jsonfy

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
    description =  request.get_json()['description'] #NEW adesso abbiamo unfile json che viene interpretatoo come un dictionary 
                                                     #    dal quale possiamo prendere il valore che ci interessa utilizzando la key 
                                                     #    definita nel file html
    # Inseriamo il valore come abbiamo già imparato utilizzando SQLAlchemy
    new_raw = Todo(description= description)
    db.session.add(new_raw)
    db.session.commit()

    # adesso non reindiriziamo più l'utente ma
    # vogliamo un oggetto json che restituirà i dati json
    # al client. Per farlo utiliziamo il metodo jsonfy 
    # che abbiamo importato da flask
    return jsonify({
        'description': new_raw.description
    })



@app.route("/")
def index():
    # qui utiliziamo render_template in modo che gli utenti visulizzino
    # la pagina html (in questo caso) desiderata
    return render_template('index.html', data = Todo.query.all())

if __name__ == '__main__':
    app.run()
