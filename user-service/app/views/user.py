import uuid
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.extensions.database import db
from app.models import User
from app.models.schemas import UserSchema, BasicUserSchema, UserQueryArgsSchema

# Create a Blueprint for User management
blp = Blueprint('User', 'user', description='User management')


@blp.route('/')
class Users(MethodView):
    """
    Endpoint for managing multiple URLs.
    """

    @jwt_required()
    @blp.arguments(UserQueryArgsSchema, location='query')
    @blp.response(200, UserSchema(many=True))
    def get(self, args):
        """
        Get a list of Users based on query parameters.
        """
        current_user_id = uuid.UUID(get_jwt_identity())
        current_user = User.query.get_or_404(current_user_id, description="Your User have not been found")
        if current_user.role != "admin":
            abort(403, message="You are not authorized to view this user")

        return User.query.filter_by(**args)

    @blp.arguments(UserSchema)
    @blp.response(201, BasicUserSchema)
    def post(self, new_data):
        """
        Create a new User.
        """
        user = User(**new_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=e.__class__.__name__)
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(400, message=e.__class__.__name__, errors=message)
        return user
    
@blp.route('/<uuid:id>')
class UserById(MethodView):
    """
    Endpoint for managing a single users by its id.
    """
    @jwt_required()
    @blp.response(200, BasicUserSchema)
    def get(self, id):
        """
        Get details of a User by its id.
        """
        current_user_id = uuid.UUID(get_jwt_identity())

        if current_user_id != id:
            current_user = User.query.get_or_404(id, description="Your User have not been found")
            if current_user.role != "admin":
                abort(403, message="You are not authorized to view this user")

        user = User.query.get_or_404(id, description="User not found")
        return user
    
    @jwt_required()
    @blp.response(200, BasicUserSchema)
    def put(self, id):
        """
        Update details of a User  by its id.
        """
        current_user_id = uuid.UUID(get_jwt_identity())

        if current_user_id != id:
            abort(403, message="You are not authorized to modify this user")

        payload = request.get_json()
        user = User.query.filter_by(id=id).first_or_404(description="User not found")

        for key in payload.keys():
            setattr(user, key, payload[key])

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(500, message=e.__class__.__name__, errors=message)

        return user
    
    @jwt_required()
    @blp.response(204, BasicUserSchema)
    def delete(self, id):
        """
        Delete a User by its id.
        """
        current_user_id = uuid.UUID(get_jwt_identity())

        if current_user_id != id:
            abort(403, message="You are not authorized to delete this user")
        
        user = User.query.filter_by(id=id).first_or_404(description="User not found")
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(500, message=e.__class__.__name__, errors=message)
        return {}

@blp.route('/login')
class Users(MethodView):
    """
    Endpoint for login.
    """

    @blp.arguments(UserSchema(only=('username', 'password')))
    @blp.response(200)
    def post(self, args):
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            # Generate access token (JWT) using user's ID as the identity and role
            additional_claims = {
                'role': user.role
            }
            access_token = create_access_token(identity=user.id,additional_claims=additional_claims)
            return jsonify(access_token=access_token)
        else:
            abort(401, message='Invalid username or password')