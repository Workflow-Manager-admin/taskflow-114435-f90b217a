from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models import db, User
from app.schemas import UserSignupSchema, UserSigninSchema, UserSchema
from app.auth_utils import hash_password, verify_password, generate_token

blp = Blueprint(
    "Users",
    "users",
    url_prefix="/api/users",
    description="Endpoints for user signup and authentication"
)

# PUBLIC_INTERFACE
@blp.route("/signup")
class Signup(MethodView):
    """User signup endpoint"""
    @blp.arguments(UserSignupSchema)
    @blp.response(201, UserSchema)
    def post(self, new_user_data):
        username = new_user_data["username"]
        password = new_user_data["password"]

        if User.query.filter_by(username=username).first():
            abort(409, message="Username already taken.")

        user = User(username=username, password_hash=hash_password(password))
        db.session.add(user)
        db.session.commit()
        return user

# PUBLIC_INTERFACE
@blp.route("/signin")
class Signin(MethodView):
    """User signin endpoint"""
    @blp.arguments(UserSigninSchema)
    def post(self, credentials):
        username = credentials["username"]
        password = credentials["password"]
        user = User.query.filter_by(username=username).first()
        if not user or not verify_password(password, user.password_hash):
            abort(401, message="Invalid username or password")
        token = generate_token(user.id)
        return {"token": token, "user": UserSchema().dump(user)}
