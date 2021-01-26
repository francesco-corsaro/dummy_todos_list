# in questo file utiliziamo la librerira SQLAlchemy per fare
# un select * della tabella
from flask import Flask,render_template  
# usiamo la libreria render_template ^   
# questa libreria ci permette divisualizzare
# file html, xml xhml

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



@app.route("/")
def index():
    # qui utiliziamo render_template in momdo che gli utenti visulizzino
    # la pagina html (in questo caso) desiderata
    return render_template('index.html', data = Todo.query.all())

if __name__ == '__main__':
    app.run()
