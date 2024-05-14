import marshmallow as mar
from marshmallow_sqlalchemy import field_for

from app.extensions.database import ma
from app.models import User

"""class DefaultSchema(ma.SQLAlchemySchema):
    class Meta:
        include_fk = True

    def update(self, obj, data):
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))"""

class UserSchema(ma.SQLAlchemySchema):
    """
    Schema for serializing and deserializing Url model objects.
    """
    class Meta:
        model = User
        ordered = True
        unknown = mar.EXCLUDE

    id = field_for(User, "id", dump_only=True)
    username = field_for(User, "username", required=True)
    email = field_for(User, "email", required=True)
    password = field_for(User, "password", load_only=True)  # Load only for security
    is_admin = field_for(User, "is_admin", default=False)
    is_active = field_for(User, "is_active", default=True)
    created_at = field_for(User, "created_at", dump_only=True)
    updated_at = field_for(User, "updated_at", dump_only=True)

    """def update(self, obj, data):
        # Update object nullifying missing data
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))"""

class BasicUserSchema(UserSchema):
    class Meta(UserSchema.Meta):
        exclude = ("password", "is_admin")

class AdminUserSchema(UserSchema):
    class Meta(UserSchema.Meta):
        exclude = ("password",)


class UserQueryArgsSchema(ma.Schema):
    username = mar.fields.Str()
    email = mar.fields.Str()
    team_id = mar.fields.UUID()