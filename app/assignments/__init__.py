from flask import Blueprint

assignments_bp = Blueprint("assignments", __name__, url_prefix="/assignments")

from app.assignments import routes