from flask import Blueprint

contracts_bp = Blueprint("contracts", __name__, url_prefix="/contracts")

from app.contracts import routes