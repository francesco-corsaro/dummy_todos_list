# Adesso prendiamo i dati che inseriti dall'utente
from flask import Flask,render_template, request, redirect, url_for
# usiamo la libreria                    request^  redirect e url_for
# request: ci permette di prendere i dati che provengono dalla view
# redirect: direziona la route 
# url_for: diamo la url

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
##### IL NUOVO CODICE INIZIA DA QUA #####
# Per prima cosa impostamo la route, la definizmoa in base all'action
# che abbiamo scritto nel form HTML, e specifichiamo anche il method utilizzato

@app.route('/todos/create', methods=['POST'])

# poi creiamo un handler per gestire quello che succede su /todos/create
def create_todo():
    description =  request.form.get('description') # prendiamo il valore di description con request.form
    
    # Inseriamo il valore come abbiamo già imparato utilizzando SQLAlchemy
    new_raw = Todo(description= description)
    db.session.add(new_raw)
    db.session.commit()

    # adesso diciamo al programma di dirigere l'utente 
    # alla nostra index che aggiornerà la view con i dati appena inseriti.
    # L'argomento di url_for è il nome della funzione che gestisce la view 
    # dell'index
    return redirect(url_for('index'))



@app.route("/")
def index():
    # qui utiliziamo render_template in modo che gli utenti visulizzino
    # la pagina html (in questo caso) desiderata
    return render_template('index.html', data = Todo.query.all())

if __name__ == '__main__':
    app.run()
