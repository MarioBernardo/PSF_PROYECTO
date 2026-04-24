from flask import Blueprint

delays_bp = Blueprint("delays", __name__, url_prefix="/delays")

from app.delays import routes