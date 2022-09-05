import random
from datetime import timedelta
import traceback
from flask_restful import Resource
from flask import request
from flask_bcrypt import  generate_password_hash, check_password_hash
from flask_jwt_extended import (
                create_access_token,
                jwt_required,
                get_jwt_identity
                )

from models.user import UserModel
from schemas.user import UserSchema

import app
user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        user_json = request.get_json()
        user = user_schema.load(user_json, partial=("number","expire_at","repeat_password"))
        if UserModel.check_username(user.username):
            return {"message":" A username not found"}, 404

        if UserModel.check_email(user.email):
            return {"message":" A email not found"}, 404
            
        if UserModel.check_phone(user.phone):
            return {"message":" A phone not found"}, 404        
        
        if UserModel.check_name(user.name):
            return {"message":" A name not found"}, 404

        if UserModel.check_password(user.password):
            return {"message":" A password not found"}, 404
            
        if UserModel.find_by_username(user.username):
            return {"message":" A user with that username already exists"}, 400

        if UserModel.find_by_email(user.email):
            return {"message":" A user with that email already exists"}, 400

        if UserModel.find_by_phone(user.phone):
            return {"message":" A user with that phone already exists"}, 400

        user.password = generate_password_hash(user.password)
        
        user.repeat_password = user.password
        try:
            access_token = create_access_token(identity=user.phone, expires_delta=timedelta(seconds=1200))
            user.number = random.randint(100000,999999)
        
            user.save_to_db()
            app.index(user)
            return{
                'access_token':access_token
            }
        except:
            traceback.print_exc()
            return {"message":"FAILED_TO_CREATE"}, 500


class UserConfirm(Resource):
    @jwt_required()
    def post(self):
        user_phone = get_jwt_identity()
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email","phone","name","password", "username", "expire_at", "repeat_password"))
        user_number = UserModel.find_by_number(user_data.number)
    
        find_phone= UserModel.find_by_phone(user_phone)
        if not (find_phone and user_number):
                # if not user_number:
            return {"message": "NOT_FOUND"}, 404

        if user_number.expired:
            user_number.save_to_db()
            return {"message": "EXPIRED"}, 400
        user_number.activated = True
        user_number.save_to_db()
        access_token = create_access_token(identity=find_phone.id, expires_delta=timedelta(seconds=600))
        
        return{

            'access_token':access_token
        }


class UserLogin(Resource):
    def post(self):
        
        user_json = request.get_json()
        user = user_schema.load(user_json, partial=("email","phone","name","number" ,"expire_at", "repeat_password"))

        find_user = UserModel.find_by_username(user.username)


        if find_user and (check_password_hash(find_user.password, user.password)):

            find_user.number = random.randint(100000,999999)
            find_user.save_to_db()
            app.index(find_user)
            access_token = create_access_token(identity=find_user.phone, expires_delta=timedelta(seconds=1200))
            return{
                'access_token':access_token
            }, 200
        return {'message': 'invalid credentials'}, 401


class forgot_password(Resource):
    def post(self):
        user_json = request.get_json()
        user = user_schema.load(user_json, partial=("username","password","phone","name","number" ,"expire_at", "repeat_password"))

        find_email = UserModel.find_by_email(user.email)
        if find_email:
            find_email.number = random.randint(100000,999999)
            find_email.save_to_db()
            app.index(find_email)
            access_token = create_access_token(identity=find_email.phone, expires_delta=timedelta(seconds=1200))
            return{
                'access_token':access_token
            }, 200
        return {'message': 'email not found'}, 404
        


class change_password(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user_json = request.get_json()
        user = user_schema.load(user_json, partial=("username","email","phone","name","number" ,"expire_at"))
        find_id= UserModel.find_by_id(user_id)
        if not find_id:
            return {"message": "NOT_FOUND"}, 401
        else:
            find_id.password = user.password
            
            find_id.repeat_password = user.repeat_password
            if find_id.password == find_id.repeat_password:
                find_id.password = generate_password_hash(user.password)
                find_id.repeat_password = find_id.password

                find_id.save_to_db()

            
                return {"message":"change"}, 200
            else:
                print(find_id.password)
                return {"message":"password not match together"}, 400
        

