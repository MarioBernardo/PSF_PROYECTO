from flask import Blueprint

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")

from app.clients import routes