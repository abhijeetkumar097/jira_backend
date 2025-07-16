from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from flask import jsonify

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()
            if user.get("role") not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Access forbidden: insufficient permissions"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
