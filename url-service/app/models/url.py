import uuid
import sqlalchemy_utils

from app.extensions.database import db

class UrlModel(db.Model):
    """
    Model class for representing shortened URL entries in the database
    """

    __tablename__ = "urls"

    # Define columns for the Url table
    id = db.Column(sqlalchemy_utils.types.uuid.UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    owner_id = db.Column(sqlalchemy_utils.types.uuid.UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    url_key = db.Column(db.String, unique=True, nullable=False)
    redirect_url = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
