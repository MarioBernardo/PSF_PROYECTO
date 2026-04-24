from flask import Blueprint

exports_bp = Blueprint(
    "exports",
    __name__,
    url_prefix="/exports"
)

from app.exports import routes