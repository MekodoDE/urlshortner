import marshmallow as mar
from marshmallow_sqlalchemy import field_for

from app.extensions.database import ma
from app.models import Url

class UrlSchema(ma.SQLAlchemySchema):
    """
    Schema for serializing and deserializing Url model objects.
    """

    class Meta:
        model = Url
        ordered = True
        unknown = mar.EXCLUDE

    # Fields to include in the schema
    id = field_for(Url, "id", dump_only=True)
    owner_id = field_for(Url, "owner_id", required=True)
    url_key = field_for(Url, "url_key")
    redirect_url = field_for(Url, "redirect_url", required=True)
    is_disabled = field_for(Url, "is_disabled", default=False)
    created_at = field_for(Url, "created_at", dump_only=True)

class UrlQueryArgsSchema(ma.Schema):
    """
    Schema for validating query parameters for Url queries.
    """

    class Meta:
        unknown = mar.EXCLUDE

    # Define fields for query parameters
    url_key = mar.fields.Str()
