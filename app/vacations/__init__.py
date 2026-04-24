from flask import Blueprint

vacations_bp = Blueprint("vacations", __name__, url_prefix="/vacations")

from app.vacations import routes