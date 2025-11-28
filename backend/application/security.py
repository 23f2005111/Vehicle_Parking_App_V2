from flask_jwt_extended import JWTManager
from application.models import User

jwt = JWTManager()  # object creation

@jwt.user_identity_loader  # identifies the User from db
def load(user):
    return user.email  # Using username as identity

@jwt.user_lookup_loader   # gives info on user and loads the user
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()