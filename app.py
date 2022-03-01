from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/sepomex_beta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_state = db.Column(db.Text)
    capital = db.Column(db.Text)
    municipalities = db.relationship('Municipality', backref='state', lazy=True)

    def __init__(self, name_state, capital):
        self.name_state = name_state
        self.capital = capital


class Municipality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    def __init__(self, name):
        self.name = name


class Colony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postalcode = db.Column(db.Integer)
    name_colony = db.Column(db.Text)
    type_colony = db.Column(db.Text)
    type_zone = db.Column(db.Text)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    def __init__(self, postalcode, name_colony, type_colony, type_zone):
        self.postalcode = postalcode
        self.name_colony = name_colony
        self.type_colony = type_colony
        self.type_zone = type_zone


db.create_all()


class StateSchema(ma.Schema):
    class Meta:
        fields = "name"


class MunicipalitySchema(ma.Schema):
    class Meta:
        fields = "name"


class ColonySchema(ma.Schema):
    class Meta:
        fields = ("postalcode", "name_colony", "type_colony", "type_zone")




@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
