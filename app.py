import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_mail import Mail, Message


from ma import ma
from resources.user import UserRegister, UserLogin, UserAuth,UserConfirm, forgot_password, change_password
from schemas.user import UserSchema
user_schema = UserSchema()

app = Flask(__name__)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.secret_key = 'jose'
api = Api(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] =  os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.before_first_request
def create_tables():
    db.create_all()




def index(user):
    msg = Message(

                    subject='Hello',
                    sender =os.environ.get('MAIL_USERNAME'),
                    recipients = [user.email]
                )

    msg.body = str(user.number)
    mail.send(msg)
    return 'Sent'


jwt = JWTManager(app) #/auth

@jwt.token_verification_loader
def verify_token(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature varification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401

# api.add_resource(UserAuth, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')

api.add_resource(UserConfirm, '/user_confirm')
api.add_resource(forgot_password, '/forgot_password')
api.add_resource(change_password, '/change_password')

from db import db
db.init_app(app)
if __name__ == '__main__':
    ma.init_app(app)
    app.run(port=5000, debug=True)