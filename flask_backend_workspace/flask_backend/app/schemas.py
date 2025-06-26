from marshmallow import Schema, fields, validate, validates, ValidationError

# PUBLIC_INTERFACE
class UserSignupSchema(Schema):
    """Request body for user signup"""
    username = fields.String(required=True, validate=validate.Length(min=3, max=64), description="Unique username")
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=128), description="Password")

# PUBLIC_INTERFACE
class UserSigninSchema(Schema):
    """Request body for user signin"""
    username = fields.String(required=True, description="Username")
    password = fields.String(required=True, load_only=True, description="Password")

# PUBLIC_INTERFACE
class UserSchema(Schema):
    """Serialized output for a user"""
    id = fields.Integer()
    username = fields.String()
    created_at = fields.DateTime()

# PUBLIC_INTERFACE
class TaskInputSchema(Schema):
    """Schema for creating/updating a task"""
    title = fields.String(required=True, validate=validate.Length(min=1, max=128))
    description = fields.String(missing='', allow_none=True)
    completed = fields.Boolean(missing=False)

# PUBLIC_INTERFACE
class TaskSchema(Schema):
    """Serialized output for a task"""
    id = fields.Integer()
    user_id = fields.Integer()
    title = fields.String()
    description = fields.String()
    completed = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime(allow_none=True)
