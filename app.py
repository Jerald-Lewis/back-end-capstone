import email
from flask import Flask, request, jsonify
# from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
import os

from flask_cors import CORS
from sqlalchemy import ForeignKey

app=Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
# redis = FlaskRedis(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

users_table = db.Table('users_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('admin_id', db.Integer, db.ForeignKey('admin.admin_id'))
    )


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    assets = db.relationship('Asset', backref='user', lazy=True)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Admin(User):
    __tablename__ = 'admin'
    
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_email = db.Column(db.String, unique=True, nullable=False)
    admin_password = db.Column(db.String, nullable=False)
    admin_first_name = db.Column(db.String, nullable=False)
    admin_last_name = db.Column(db.String, nullable=False)
    can_access = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __init__(self, email, password, first_name, last_name, can_acess, user_id):
        super().__init__(email, password, first_name, last_name)
        self.admin_email = email
        self.admin_password = password
        self.admin_first_name = first_name
        self.admin_last_name = last_name
        self.admin_can_access = can_acess
        self.user_id = user_id

@app.route('/user/add', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')

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

@app.route('/user/verify', methods=['POST'])
def verify_user():
    # if request.content_type != 'application/json':
    #     return jsonify('Error: Data must be json')

    post_data = request.get_json()
    post_data = post_data['body']
    email = post_data['email']
    password = post_data['password']
    user = db.session.query(User).filter(User.email == email).first()
    if email is None:
        return jsonify("User NOT verified")

    if bcrypt.check_password_hash(user.password, password) == False:
        return jsonify("User NOT verified")
    
    return jsonify("User has been verified!")

@app.route('/user/checklogin', methods=['GET'])
def check_logged_in():
    # post_data = request.get_json()
    # print(post_data)
    user = db.session.query(User).filter(User.email == email).first()
    #     # check_logged_in_status =
    return jsonify("this request works")

class Asset(db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.Integer, primary_key=True)
    computer_name = db.Column(db.String(8), nullable=False, unique=True)
    service_tag = db.Column(db.String(7), nullable=False, unique=True)
    status = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, computer_name, service_tag, status, location):
        self.computer_name = computer_name
        self.service_tag = service_tag
        self.status = status
        self.location = location

@app.route('/asset/add', methods=["POST"])
def add_asset():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    computer_name = post_data.get('computer_name')
    service_tag = post_data.get('service_tag')
    status = post_data.get('status')
    location = post_data.get('location')
    user_id = post_data.get('user_id')

    asset = db.session.query(Asset).filter(Asset.computer_name == computer_name).first()

    if computer_name == None:
        return jsonify("Error: Data must have a 'computer_name' key.")

    if asset:
        return jsonify("Error: computer name must be unique")

    if location == None:
        return jsonify("Error: Data must have a 'location' key.")

    
    new_asset = Asset(computer_name, service_tag, status, location, user_id)
    db.session.add(new_asset)
    db.session.commit()

    return jsonify("You've added a new asset!")

@app.route('/asset/get', methods=["GET"])
def get_assets():
    assets = db.session.query(Asset).all()
    return jsonify(multiple_assets_schema.dump(assets))

@app.route('/asset/get/<id>', methods=["GET"])
def get_asset(id):
    asset = db.session.query(Asset).filter(Asset.id == id).first()
    return jsonify(assets_schema.dump(asset))


@app.route('/asset/get/computername/<computer_name>', methods=["GET"])
def get_asset_by_computer_name(computer_name):
    asset = db.session.query(Asset).filter(Asset.computer_name == computer_name).first()
    return jsonify(assets_schema.dump(asset))

@app.route('/asset/delete/<id>', methods=["DELETE"])
def delete_asset_by_id(id):
    asset = db.session.query(Asset).filter(Asset.id == id).first()
    db.session.delete(asset)
    db.session.commit()
    
    return jsonify("The book has been deleted.")

@app.route('/asset/update/<id>', methods=["PUT", "PATCH"])
def update_asset_by_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    computer_name = post_data.get('computer_name')
    service_tag = post_data.get('service_tag')
    status = post_data.get('status')
    location = post_data.get('location')

    asset = db.session.query(Asset).filter(Asset.id == id).first()

    if computer_name != None:
        asset.computer_name = computer_name
    if service_tag != None:
        asset.service_tag = service_tag
    if status != None:
        asset.status = status
    if location != None:
        asset.location = location

    db.session.commit()
    return jsonify("Asset has been updated!")

class AssetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'computer_name', 'service_tag', 'status', 'location')
assets_schema = AssetSchema()
multiple_assets_schema = AssetSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

if __name__ == "__main__":
    app.run(debug=True) 

    # user schema nest stock room, 