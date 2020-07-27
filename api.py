from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
import pyotp

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
totp = pyotp.TOTP('base32secret3232')

class UserModel(db.Model):
    username = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User(name = {name}, password = {password})"

db.create_all()

details = reqparse.RequestParser()
details.add_argument("name", type=str, help="Name of the User", required=True)
details.add_argument("password", type=str, help="Password of the User", required=True)
details.add_argument("otp", type=int, help="OTP of the User", required=True)

details_update = reqparse.RequestParser()
details_update.add_argument("name", type=str, help="Name of the User")
details_update.add_argument("password", type=str, help="Password of the User")
details.add_argument("otp", type=int, help="OTP of the User", required=True)

resource_fields = {
    'username' : fields.String,
    'name' : fields.String,
    'password' : fields.String,
    'otp' : fields.Integer
}

class User(Resource):
    @marshal_with(resource_fields)
    def get(self, username):
        result = UserModel.query.filter_by(username=username).first()
        if not result:
            abort(404, message="Username not found")
        return result

    @marshal_with(resource_fields)
    def put(self, username):
        args = details.parse_args()
        if args['otp'] == totp.now():
            result = UserModel.query.filter_by(username=username).first()
            if result:
                abort(409, message="Username already exists")
            user = UserModel(username=username, name=args['name'], password=args['password'])
            db.session.add(user)
            db.session.commit()
            return user, 201

    @marshal_with(resource_fields)
    def patch(self, username):
        args = details.parse_args()
        if args['otp'] == totp.now():
            result = UserModel.query.filter_by(username=username).first()
            if not result:
                abort(404, message="Username does not exist, can't update")
            
            if args['name']:
                result.name = args['name']
            if args['password']:
                result.password = args['password']

            db.session.commit()
            return result

api.add_resource(User, "/user/<string:username>")

if __name__ == "__main__":
    app.run(debug=True)
