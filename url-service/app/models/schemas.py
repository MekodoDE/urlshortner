import marshmallow as mar
from marshmallow_sqlalchemy import field_for

from app.extensions.database import ma
from app.models import UrlModel

class UrlSchema(ma.SQLAlchemySchema):
    """
    Schema for serializing and deserializing Url model objects.
    """

    class Meta:
        model = UrlModel
        ordered = True
        unknown = mar.EXCLUDE

    # Fields to include in the schema
    id = field_for(UrlModel, "id", dump_only=True)
    owner_id = field_for(UrlModel, "owner_id", required=True)
    url_key = field_for(UrlModel, "url_key")
    redirect_url = field_for(UrlModel, "redirect_url", required=True)
    is_active = field_for(UrlModel, "is_active", dump_default=True)
    created_at = field_for(UrlModel, "created_at", dump_only=True)

class UrlQueryArgsSchema(ma.Schema):
    """
    Schema for validating query parameters for Url queries.
    """

    class Meta:
        unknown = mar.EXCLUDE

    # Define fields for query parameters
    url_key = mar.fields.Str()
