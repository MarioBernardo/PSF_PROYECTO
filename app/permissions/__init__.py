from flask import Blueprint

permissions_bp = Blueprint("permissions", __name__, url_prefix="/permissions")

from app.permissions import routes