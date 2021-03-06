# Questo file è l'evoluzione dei file precedenti
# questa volta styudiamo in concetto di relazione tra le tabelle
# prima avevamo una sola tabella con le cosa da fare adesso impostiamo
# una nuova tabella genitore che contiene il titolo della categoria delle cose da fare
# Per esempio in una tabella mettima "spesa" nella tabella figlio mettiamo gli articoli da comprare
# nella tabella genitore mettimao "palestra" e nella figlio gli esercizi da fare
from flask import Flask,render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys # libreria per gestire gli errori

from flask_migrate import Migrate


app= Flask(__name__)  # crea un'aplicazione che prende il  nome del nostro file
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://fra3@localhost:5432/eg_sql_alchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

migrate= Migrate(app,db)
## Qui stiamo definendo le nostre tabelle 
# tabella genitore


class Todo_title(db.Model):
    __tablename__= 'todos_titles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    # qui definiamo la relazione con la tabella figlia
    todos= db.relationship('Tododb ', backref='todos_titles', lazy=True)
    # 1) chiamiamo la variabile con il nome della classe figlio
    # 2) utiliziamo la parola chiave db.relationship per dire a sqlAlchemy della ralazione
    # 3) tra virgolette inseriamo il nome della tabella figlio 
    # 4) impostimao una variabile denominata 'backref' e gli assegnamo il nome della tabella genitore
    # 5) è possibile impostare differenti opzioni facoltative 

    def __repr__(self):
        return "<Person ID: {}, title: {}>".format(self.id,self.title)

# Qua definiamo la tabella figlio, quasta tabella contiene le cose da fare di una determinata categoria
# infatti avra un vincolo con la tabella genitore. 
# Impostiamo una colonna per la chiave esterna che corrisponde all'id della tabella genitore
class Todo(db.Model):
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    # qui impostiamo la chiave esterna
    todo_title_id= db.Column(db.Integer, db.ForeignKey('todos_titles.id'), nullable=False)

    def __repr__(self):
        return "<Person ID: {}, description: {}>".format(self.id,self.description)

# db.create_all()  ## non abbiamo piùbisogno di questa funzione

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
        # questa è una prova che tenta di recuperare l'id 
        id_new_raw = Todo.query.filter(Todo.description==description).first()
        print(id_new_raw.id)
        body['id']=id_new_raw.id
        
        
        return jsonify(body) # questo è l'oggetto json 

###  prendiamo la variabile completato dalla view e aggiorniamo il nostro database ###

@app.route('/todos/<todo_id>/set-completed', methods=['POST']) # faccio una chiamata al percorso interessato. Da notare che todo_id è fra <>.
                                                               # questo perchè è una variabile che passimao dal file index al file app

# creo un handler per gestire quello che succede su /todos/set-completed
def updat_completed(todo_id):
    
    try:
        completed=request.get_json()['completed']
        print('completed', completed)
        #inseriamo il dato nel database
        todo= Todo.query.get(todo_id) # todo è un oggetto che ha le proprietà della riga corrispondete all'id selezionato dall'utente
        todo.completed= completed   # QUESTA È UNA DELLE FUNZIONALITÀ PIÙ BELLE SQLALCHEMY
                                    # per aggionrare una riga con dei valore già esistenti basta chiamare quella riga ( con il codice sopra)
                                    # e assegnare il valore desiderato. NON VIENE UTILIZZATO NESSUN CODICE SQL
        db.session.commit()

        
    except: #in caso di errore lo gestiamo
        
        db.session.rollback()  # ci permete di evitare che dati in sospeso vengano inseriti
        
    finally: # nel finally chiudiamo la sessione
        db.session.close()
    
    return redirect(url_for('index'))
### QUI METTO LA FUNZIONE PER CANCELLARE L'ITEM DESIDERATO ###
@app.route("/todos/item_del", methods=['POST'])

def delete_item():
    try:
        deleted= request.get_json()['deletedItem']
        Todo.query.filter(Todo.id==deleted).delete()

        db.session.commit()
    except: #in caso di errore lo gestiamo
        
        db.session.rollback()  # ci permete di evitare che dati in sospeso vengano inseriti
        
    finally: # nel finally chiudiamo la sessione
        db.session.close()
    
    return redirect(url_for('index'))
    
@app.route("/")
def index():
    # qui utiliziamo render_template in modo che gli utenti visulizzino
    # la pagina html (in questo caso) desiderata
    return render_template('index.html', data = Todo.query.order_by('id').all())

if __name__ == '__main__':
    app.run()
