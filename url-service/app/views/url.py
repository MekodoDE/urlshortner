from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import json

from app.extensions.database import db
from app.models import Url
from app.models.schemas import UrlSchema, UrlQueryArgsSchema

# Create a Blueprint for URL management
blp = Blueprint('Url', 'url', description='URL management')

@blp.route('/')
class Urls(MethodView):
    """
    Endpoint for managing multiple URLs.
    """

    @blp.arguments(UrlQueryArgsSchema, location='query')
    @blp.response(200, UrlSchema(many=True))
    def get(self, args):
        """
        Get a list of URLs based on query parameters.
        """
        return Url.query.filter_by(**args)

    @blp.arguments(UrlSchema)
    @blp.response(201, UrlSchema)
    def post(self, new_data):
        """
        Create a new URL.
        """
        url = Url(**new_data)
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
        url = Url.query.filter_by(url_key=url_key)
        return url.first_or_404(description="URL key not found")
    
    @blp.response(200, UrlSchema)
    def put(self, url_key):
        """
        Update details of a URL by its key.
        """
        payload = request.get_json()
        url = Url.query.filter_by(url_key=url_key).first_or_404(description="URL key not found")

        for key in payload.keys():
            setattr(url, key, payload[key])

        try:
            db.session.add(url)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(500, message=e.__class__.__name__, errors=message)

        return url
    
    @blp.response(200, UrlSchema)
    def delete(self, url_key):
        """
        Delete a URL by its key.
        """
        url = Url.query.filter_by(url_key=url_key).first_or_404(description="URL key not found")

        try:
            db.session.delete(url)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = [str(x) for x in e.args]
            abort(500, message=e.__class__.__name__, errors=message)
        return {}
