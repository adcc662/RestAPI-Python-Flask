from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:secret@db/sepomex_beta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_state = db.Column(db.Text)
    capital = db.Column(db.Text)
    municipalities = db.relationship('Municipality', backref='state', lazy=True)
    colonies = db.relationship('Colony', backref='state', lazy=True)

    def __init__(self, id, name_state, capital):
        self.id = id
        self.name_state = name_state
        self.capital = capital


class Municipality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    def __init__(self, name, state_id):
        self.name = name
        self.state_id = state_id


class Colony(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postalcode = db.Column(db.Integer)
    name_colony = db.Column(db.Text)
    type_colony = db.Column(db.Text)
    type_zone = db.Column(db.Text)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    def __init__(self, postalcode, name_colony, type_colony, type_zone, state_id):
        self.postalcode = postalcode
        self.name_colony = name_colony
        self.type_colony = type_colony
        self.type_zone = type_zone
        self.state_id = state_id


db.create_all()


class StateSchema(ma.Schema):
    class Meta:
        fields = ("id", "name_state", "capital")


class MunicipalitySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "state_id")


class ColonySchema(ma.Schema):
    class Meta:
        fields = ("id", "postalcode", "name_colony", "type_colony", "type_zone", "state_id")


state_schema = StateSchema()
states_schema = StateSchema(many=True)
municipality_schema = MunicipalitySchema()
municipalities_schema = MunicipalitySchema(many=True)
colony_schema = ColonySchema()
colonies_schema = ColonySchema(many=True)


@app.route('/')
def hello_world():  # put application's code here
    return 'SEPOMEX'


@app.route('/states', methods=["POST"])
def create_state():
    #    print(request.json)
    #    return 'received'
    name_state = request.json['name_state']
    capital = request.json['capital']
    new_state = State(name_state, capital)
    db.session.add(new_state)
    db.session.commit()
    return state_schema.jsonify(new_state)


@app.route('/states', methods=["GET"])
def get_states():
    all_states = State.query.all()
    result = states_schema.dump(all_states)
    return jsonify(result)


@app.route('/municipalities', methods=["POST"])
def create_municipalities():
    name = request.json['name']
    state_id = request.json['state_id']
    new_municipality = Municipality(name, state_id)
    db.session.add(new_municipality)
    db.session.commit()
    return municipality_schema.jsonify(new_municipality)


@app.route('/municipalities', methods=["GET"])
def get_municipalities():
    all_municipalities = Municipality.query.all()
    result = municipalities_schema.dump(all_municipalities)
    return jsonify(result)


@app.route('/colonies', methods=["POST"])
def create_colonies():
    postalcode = request.json['postalcode']
    name_colony = request.json['name_colony']
    type_colony = request.json['type_colony']
    type_zone = request.json['type_zone']
    state_id = request.json['state_id']
    new_colony = Colony(postalcode, name_colony, type_colony, type_zone, state_id)
    db.session.add(new_colony)
    db.session.commit()
    return colony_schema.jsonify(new_colony)


@app.route('/colonies', methods=["GET"])
def get_colonies():
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None:
        limit = 10
    if offset is None:
        offset = 0
    all_colonies = Colony.query.limit(limit).offset(offset)
    result = colonies_schema.dump(all_colonies)
    return jsonify(result)


@app.route('/colonies/<cp>', methods=["GET"])
def get_colonies_by_cp(cp):
    colonies = Colony.query.filter_by(postalcode=cp).all()
    result = colonies_schema.dump(colonies)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
