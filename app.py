# Questo file è l'evoluzione dei file precedenti
# continuaimo la lezione sulle relazioni fra le tabelle e quesa volta
# analizzeremo in dettaglio come fare in modo che l'utnete visualizzi le 
# 'cose da fare' riferite a una determinata categoria.
# 
# Il database è formato da due tabelle:
#  TABELLA GENITORE: >todos_titles 
#       in questa tablla salviamo il nome della categoria (eg. spesa, al momento abbiamo inserito solo 'uncategorized')
#       e il suo id. Il valore Id è la chiave primaria
###################### OUTPUT psql# \d todo_titles
######                                 Table "public.todos_titles"
#    Column |       Type        | Collation | Nullable |                 Default                  
#    --------+-------------------+-----------+----------+------------------------------------------
#    id     | integer           |           | not null | nextval('todos_titles_id_seq'::regclass)
#    title  | character varying |           | not null | 
#    Indexes:
#        "todos_titles_pkey" PRIMARY KEY, btree (id)
#    Referenced by:
#        TABLE "todos" CONSTRAINT "todos_todo_title_id_fkey" FOREIGN KEY (todo_title_id) REFERENCES todos_titles(id)

#   QUESTA È  LA TABELLA FIGLIO
#                                     Table "public.todos"
#    Column     |       Type        | Collation | Nullable |              Default              
#---------------+-------------------+-----------+----------+-----------------------------------
# id            | integer           |           | not null | nextval('todos_id_seq'::regclass)
# description   | character varying |           | not null | 
# completed     | boolean           |           | not null | 
# todo_title_id | integer           |           | not null | 
#Indexes:
#    "todos_pkey" PRIMARY KEY, btree (id)
#Foreign-key constraints:
#    "todos_todo_title_id_fkey" FOREIGN KEY (todo_title_id) REFERENCES todos_titles(id)


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
    todos= db.relationship('Todo', backref='todos_titles', lazy=True)
    # 1) chiamiamo la variabile con il nome della classe figlio
    # 2) utiliziamo la parola chiave db.relationship per dire a sqlAlchemy della ralazione
    # 3) tra virgolette inseriamo il nome della tabella figlio 
    # 4) impostimao una variabile denominata 'backref' e gli assegnamo il nome della tabella genitore
    # 5) è possibile impostare differenti opzioni facoltative 

    def __repr__(self):
        return "<todos_titles ID: {}, title: {}>".format(self.id,self.title)

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
    # Lesson by Juliano. é possible utilizzare un 'cascade behaviour' che permette
    # di cancellare la riga della tabella genitore e a cascata le righe delle tabelle figlio ad esso associate
    # per fare questo impostiamo sulla tabella figlia una relatioship con la parola chiave
    # cascade impostata su 'all, delete'
    todo_title= db.relationship('Todo_title', backref=db.backref('todos_todo_title',cascade="all, delete"))

    def __repr__(self):
        return "<todos ID: {}, description: {}>".format(self.id,self.description)

# db.create_all()  ## non abbiamo piùbisogno di questa funzione

@app.route('/todos/create', methods=['POST'])

# poi creiamo un handler per gestire quello che succede su /todos/create
def create_todo():
    error= False
    body={}
    try:
        description =  request.get_json()['description'] # questo prende i dati dal client
         
        new_raw = Todo(description= description) # questa è la procedura per inserire i dati nel database
        # sotto impostiamo la categoria di appartenenza dell'item
        todo_id= request.get_json()['todo_title_id']
        new_raw.todo_title_id=todo_id
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

######### NEW ##########
# l'obbiettivo è far visualizzare all'utnete il file index.html con i dati estratti in base al  todo_title_id 
# che rappresenta il nostro vincolo id relazione. la funzione sarà
# simile alla funzione index precedente però in questa insirmao una variabile che ci permette di selezionare 
# quale categoria di 'cose da fare' devono esere visualizzate 

# per prima cosa definiamo un path e una variabile che ci consete 
# di selezionare la categoria delle 'cose da fare'
@app.route("/list/<todo_title_id>") 
def get_todos_categorized(todo_title_id ):
    # rispetto alla funzione index del file precendete, 
    # questa volta stiamo passando la variabile list_id per filtrare i risultati da stampare a video
    # in più aggiungiamo la variabile lists che preleva i dati dalla tabella todos_title    
    return render_template('index.html',
    lists=Todo_title.query.all(),
    active_category = Todo_title.query.get(todo_title_id),
    data = Todo.query.filter_by(todo_title_id =todo_title_id ).order_by('id').all())

### NEW FUNCTION TO CREATE NEW CATEGORY ###
@app.route('/todos_titles/create', methods=['POST'])

def create_todos_titles():
    error= False
    body={}
    try:
        title=request.get_json()['title'] #prendo il nome della nuova dal client
        new_raw= Todo_title(title=title)
        db.session.add(new_raw)
        db.session.commit()
        body['title']=new_raw.title
        body['id']=new_raw.id
    except:
        error= True
        db.session.rollback()  # ci permete di evitare che dati in sospeso vengano inseriti
        print(sys.exc_info())
    finally: # nel finally chiudiamo la sessione
        db.session.close()
    if error:
        abort(400)
    else:
        
        return jsonify(body)


#### NEW FUNCTION TO HANDLER COMPLETED CATEGORY ###
# qui inserisco la funzione per sengare  come completati glialtri item
@app.route('/todos/<todo_id>/set-categoryCompleted', methods=['POST']) 

def updat_categoryCompleted(todo_id):
    try:
        completed= request.get_json()['completed']
        items_completed= Todo.query.filter_by(todo_title_id=todo_id)
        for item in  items_completed:
            item.completed=completed
        db.session.commit()
    
    except: #in caso di errore lo gestiamo
        
        db.session.rollback()  # ci permete di evitare che dati in sospeso vengano inseriti
        
    finally: # nel finally chiudiamo la sessione
        db.session.close()
    
    return redirect(url_for('get_todos_categorized', todo_title_id=todo_id))


### function to delete the category and its children ###

@app.route("/todos/del_category", methods=['POST'])

def del_category():
    try:
        deleted= request.get_json()['deletedItem']

        # Inizialmente avevo usato i due comandi di sotto per poter cancellare 
        # i recod dei genitori e dei figli.
        #Todo.query.filter(Todo.todo_title_id==deleted).delete() # elimina i figli 
        #Todo_title.query.filter(Todo_title.id==deleted).delete() # elimina i genitori

        # Poi ho scoperto il 'cascade behaviour' quindi eliminando il genitore si eliminano i figli
        # ho creato una relatioship nella tabella figlio (vedi il model sopra)
        # e qui semplicemente:       
        category_delete= Todo_title.query.get(deleted) # seleziono il record da eliminare
        db.session.delete(category_delete) # elimino lui e i suoi figli

        db.session.commit()
    except: #in caso di errore lo gestiamo
        
        db.session.rollback()  # ci permete di evitare che dati in sospeso vengano inseriti
        
    finally: # nel finally chiudiamo la sessione
        db.session.close()
    
    return redirect(url_for('index'))
    

@app.route("/")
def index():
    # dato che il metodo render_template viene utilizzato per la funzione get_todos_categorized
    # qui facciamo un redirect alla funzione di rendering e passiamo come argomento todos_list il valore 1
    return redirect(url_for('get_todos_categorized', todo_title_id=1))

if __name__ == '__main__':
    app.run()



#>>> category_delete= Todo_title.query.get(27)
#>>> for category in category_delete.todos:
#...     db.session.delete(category)
