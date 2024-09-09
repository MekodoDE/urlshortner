import uuid
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import get_jwt, jwt_required
from flask_jwt_extended.exceptions import JWTExtendedException

from app.extensions.database import db
from app.models import UrlModel
from app.models.schemas import UrlSchema, UrlQueryArgsSchema

from .utils import generate_random_url_key

# Create a Blueprint for URL management
blp = Blueprint('Url', 'url', description='URL management')

@blp.route('/')
class Urls(MethodView):
    """
    Endpoint for managing multiple URLs.
    """

    @jwt_required()
    @blp.arguments(UrlQueryArgsSchema, location='query')
    @blp.response(200, UrlSchema(many=True))
    def get(self, args):
        """
        Get a list of URLs based on query parameters.
        """
        try:
            jwt_claims = get_jwt()
            role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        except JWTExtendedException as e:
            abort(401, message="Invalid or expired token.")  # Handle token issues specifically

        if role != "admin":
            abort(403, message="You are not authorized to perform this action")
        return UrlModel.query.filter_by(**args)

    @jwt_required()
    @blp.arguments(UrlSchema(only=["redirect_url", "url_key"]))
    @blp.response(201, UrlSchema)
    def post(self, new_data):
        """
        Create a new shortened URL with an optional custom key.
        If 'url_key' is not provided or the user is not an admin, a random key will be generated.
        """
        try:
            jwt_claims = get_jwt()
            user_id = jwt_claims.get("sub")
            role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        except JWTExtendedException as e:
            abort(401, message="Invalid or expired token.")  # Handle token issues specifically
        
        # Create new URL object and assign the owner
        url = UrlModel(**new_data)
        url.owner_id = uuid.UUID(user_id)

        # Generate a random url_key if not provided or if the user is not an admin
        if not new_data.get("url_key") or role != "admin":
            url.url_key = generate_random_url_key()
        
        try:
            db.session.add(url)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=e.__class__.__name__)
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(400, message=e.__class__.__name__, errors=message)
        return url
    
@blp.route('/<string:url_key>')
class UrlByKey(MethodView):
    """
    Endpoint for managing a single URL by its key.
    """

    @blp.response(200, UrlSchema)
    def get(self, url_key):
        """
        Get details of a URL by its key.
        """
        url = UrlModel.query.filter_by(url_key=url_key)
        return url.first_or_404(description="URL key not found.")
    
    @jwt_required()
    @blp.arguments(UrlSchema(only=["is_active", "redirect_url", "owner_id", "url_key"], partial=True))
    @blp.response(200, UrlSchema)
    def put(self, updated_data, url_key):
        """
        Update details of a URL by its key.
        """
        try:
            jwt_claims = get_jwt()
            user_id = uuid.UUID(jwt_claims.get("sub"))
            role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        except JWTExtendedException:
            abort(401, message="Invalid or expired token.")  # Handle token issues specifically

        url = UrlModel.query.filter_by(url_key=url_key).first_or_404(description="URL key not found.")

        # Authorization check: Only the owner or an admin can update the URL
        if user_id != url.owner_id and role != "admin":
            abort(403, message="You are not authorized to perform this action")

        # Update fields from the payload
        for key, value in updated_data.items():
            if key == "is_active" or role == "admin":  # Allow non-admins to only modify 'is_active'
                setattr(url, key, value)

        # Commit the changes
        try:
            db.session.add(url)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="Database error", errors=str(e))

        return url

    @jwt_required()
    @blp.response(204, UrlSchema)
    def delete(self, url_key):
        """
        Delete a URL by its key.
        """
        try:
            jwt_claims = get_jwt()
            user_id = uuid.UUID(jwt_claims.get("sub"))
            role = jwt_claims.get("role", "viewer")  # Default to 'viewer' if no role is present
        except JWTExtendedException:
            abort(401, message="Invalid or expired token.")  # Handle token issues specifically

        url = UrlModel.query.filter_by(url_key=url_key).first_or_404(description="URL key not found.")

        # Authorization check: Only the owner or an admin can update the URL
        if user_id != url.owner_id and role != "admin":
            abort(403, message="You are not authorized to perform this action")

        try:
            db.session.delete(url)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(500, message=e.__class__.__name__, errors=message)
        return {}
