import email
from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
import os

# from flask_cors import CORS

app=Flask(__name__)
bcrypt = Bcrypt(app)
redis = FlaskRedis(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    stock_room = db.relationship('StockRoom', backref='user', cascade='all, delete, delete-orphan', primaryjoin="User.id == StockRoom.user_id")

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Admin(User):
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_email = db.Column(db.String, unique=True, nullable=False)
    admin_password = db.Column(db.String, nullable=False)
    admin_first_name = db.Column(db.String, nullable=False)
    admin_last_name = db.Column(db.String, nullable=False)
    can_access = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __init__(self, email, password, first_name, last_name, can_acess):
        super().__init__(email, password, first_name, last_name)
        self.admin_email = email
        self.admin_password = password
        self.admin_first_name = first_name
        self.admin_last_name = last_name
        self.admin_can_access = can_acess

@app.route('/user/add', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    stock_room = post_data.get('stock_room')

    possible_duplicate = db.session.query(User).filter(User.email == email).first()

    if possible_duplicate is not None:
        return jsonify("Error: This email has an account set up already.")

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email, encrypted_password, first_name, last_name)

    db.session.add(new_user)
    db.session.commit()

    return jsonify("Congrats, you've signed up for an account!")

@app.route('/user/get', methods=["GET"])
def get_users():
    users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(users))

class Asset(db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.Integer, primary_key=True)
    computer_name = db.Column(db.String(8), nullable=False, unique=True)
    service_tag = db.Column(db.String(7), nullable=False, unique=True)
    status = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    stock_room = db.relationship('StockRoom', backref='asset', cascade='all, delete, delete-orphan', primaryjoin="Asset.id == StockRoom.asset_id")

    def __init__(self, computer_name, service_tag, status, location):
        self.computer_name = computer_name
        self.service_tag = service_tag
        self.status = status
        self.location = location

class StockRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)

    def __init__(self, street_address, city, state):
        self.street_address = street_address
        self.city = city
        self.state = state

class AssetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'computer_name', 'service_tag', 'status', 'location')
assets_schema = AssetSchema()
multiple_assets_schema = AssetSchema(many=True)

class StockRoomSchema(ma.Schema):
    class Meta:
        fields = ('id', 'street_address', 'city', 'state', 'assets','user_id')
    assets = ma.Nested(multiple_assets_schema)
stock_room_schema = StockRoomSchema()
multiple_stockroom_schema = StockRoomSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'stock_room')
    stock_room = ma.Nested(multiple_stockroom_schema)
user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

if __name__ == "__main__":
    app.run(debug=True) 

    # user schema nest stock room, 