from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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

    @blp.arguments(UserQueryArgsSchema, location='query')
    @blp.response(200, UserSchema(many=True))
    def get(self, args):
        """
        Get a list of Users based on query parameters.
        """
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

    @blp.response(200, UserSchema)
    def get(self, id):
        """
        Get details of a User by its id.
        """
        user = User.query.get_or_404(id, description="User not found")
        return user
    
    @blp.response(200, UserSchema)
    def put(self, id):
        """
        Update details of a User  by its id.
        """
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

        return id
    
    @blp.response(204)
    def delete(self, id):
        """
        Delete a User by its id.
        """
        user = User.query.filter_by(id=id).first_or_404(description="User not found")
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(500, message=e.__class__.__name__, errors=message)
        return {}
