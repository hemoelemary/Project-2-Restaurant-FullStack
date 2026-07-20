from flask import Flask,render_template,request,jsonify,session,redirect
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy()
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app,db)

class Products(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    image = db.Column(db.Text)
    def __init__(self,name,image):
        self.name=name
        self.image=image

@app.route('/')
def index():
    getprods = Products.query.all()
    return render_template('index.html',prods=getprods)

@app.route('/cart')
def cart():
    chosen = session['prods'] if 'prods' in session else ''
    
    names = [i['name'] for i in chosen]
    countclass = len([i for i in names if i=='classic'])
    countchees = len([i for i in names if i=='cheese'])
    counter=[]
    counterobj = {}
    for j in set(names):
        counter.append(len([i for i in names if i==j]))
    for k,j in enumerate(set(names)):
        counterobj[j]=counter[k]
    unique_chosen = []
    seen_names = set()
    for item in chosen:
        if item['name'] not in seen_names:
            seen_names.add(item['name'])
            unique_chosen.append(item)  
              
    return render_template('cart.html',prods=unique_chosen or [],classico=countclass,cheesco=countchees,counterobj=counterobj)
@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method == "POST":
        name = request.form.get('name')
        img = request.form.get('img')
        obj = Products(name,img)
        db.session.add(obj)
        db.session.commit()
        return redirect('/')

    return render_template('admin.html')

@app.route('/save',methods=["POST","GET"])
def save():
    data = request.get_json()
    if 'prods' not in session:
        session['prods'] = data
    else:
        session['prods']+=data
        session.modified=True
    return jsonify({'products':data})
@app.route('/clear')
def clearsession():
    session['prods']=[]
    return {'message':'empty'}
if __name__ == '__main__':
    app.run(debug=True)