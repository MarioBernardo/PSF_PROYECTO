from flask import Blueprint

shifts_bp = Blueprint("shifts", __name__, url_prefix="/shifts")

from app.shifts import routes