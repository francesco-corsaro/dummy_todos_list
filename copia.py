from flask import Flask,render_template 
# usiamo la libreria render_template ^   
# questa libreria ci permette divisualizzare
# file html, xml xhml
 
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)  # crea un'aplicazione che prende il  nome del nostro file
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://fra@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__= 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    
    def __repr__(self):
        return '< Todo Id:{}, Description:{}'.format(self.id, self.description)
    
db.create_all() 

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

if __name__ == '__main__':
    app.run()