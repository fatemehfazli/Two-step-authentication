from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password","repeat_password")
        dump_only = ("id","activated","expire_at")
        load_instance = True

# class UserlogSche(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = UserModel
#         load_only = ("password")
#         dump_only = ("email", "phone", "name", "number","expire_at")