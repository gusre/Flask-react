from flask import *
from flask_sqlalchemy import SQLAlchemy
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import base64



server = Flask(__name__)


server=Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@server/db'
server.config['SQLALCHEMY_ECHO'] = True
db= SQLAlchemy(server)

class User(db.Model):
    Name= db.Column(db.String(45),nullable = False)
    Contact = db.Column(db.String(10),primary_key=True)
    Photo=db.Column(db.LargeBinary, nullable = False)

    def __init__(self,b,c,d):
        self.Name = b
        self.Contact=c
        self.Photo=d

def convert_row_to_dict(x):
    d=dict()
    d['name']=x.Name
    d['contact']=x.Contact
    d['photo']=str(base64.encodebytes(x.Photo))
    return d

@server.route('/api',methods=['GET'])
def api():
    count=User.query.all()
    #converting rows brought from database to list of dicts
    arr=list(map(convert_row_to_dict,count))
    return {'data':arr}

@server.route('/datahandler', methods=['DELETE'])
def deldata():
    print(request)
    print(request.query_string)
    data=request.get_json()
    contact=data['contactnum']
    try:
        person = User.query.filter_by(Contact=contact).first()
        db.session.delete(person)
        db.session.commit()
        return {'Status':'Success'}
    except:
        return {'Status':'Fail'}

@server.route('/datahandler', methods=['PUT',])
def updatedata():
    print('---------')
    print('---------')
    data=request.get_json()
    to_update=dict()
    to_update['Name']=data['user']
    to_update['Contact']=data['contactnum']
    contact=data['old']
    print(contact)
    try:    
        User.query.filter_by(Contact=contact).update(to_update)
        db.session.commit()
        return {'Status':'Success'}
    except:
        return {'Status':'Fail'}

@server.route('/datahandler', methods=['POST'])
def insertdata():
    print(request)
    print(request.query_string)
    if request.method == 'POST':
        print(request)
        print(request.query_string)
        data=request.get_json()
        user=data['user']
        print(user)
        num=data['contactnum']
        img=data['photo']
        img=img[22:]
        photo=base64.b64decode(img) 
        new_user=User(user,num,photo)
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'Status': 'User added'})
        except:
            return jsonify({'Status': 'Image cant be proccessed,change image'})

@server.route("/dash")
@server.route("/alert")
@server.route("/note")
@server.route("/home")
@server.route('/')
def index():
    return render_template("index.html", flask_token="Hello world")

app2 =dash.Dash(
    __name__,server=server,
    routes_pathname_prefix='/dash2/'
)
df2 = pd.DataFrame({"x": [1, 2, 3], "SF": [4, 1, 2], "Montreal": [2, 4, 5]})

fig2 = px.bar(df2, x="x", y=["SF", "Montreal"], barmode="group")

app2.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig2
    )
])
if __name__ == '__main__':
    server.run(debug=True)
