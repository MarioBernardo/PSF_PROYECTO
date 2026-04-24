import os
from datetime import datetime
from flask import send_file, current_app, abort
from flask_login import login_required

from app.backup import backup_bp
from app.decorators import role_required


@backup_bp.route("/")
@login_required
@role_required("admin")
def download_backup():
    uri = current_app.config.get("SQLALCHEMY_DATABASE_URI")

    if not uri or not uri.startswith("sqlite:///"):
        abort(404, description="No se encontró una base SQLite para respaldar.")

    db_path = uri.replace("sqlite:///", "")

    # Si la ruta no es absoluta, la busca desde la raíz del proyecto
    if not os.path.isabs(db_path):
        base_dir = os.path.abspath(os.getcwd())

        posibles_rutas = [
            os.path.join(base_dir, db_path),
            os.path.join(base_dir, "instance", db_path),
        ]

        db_path = None

        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                db_path = ruta
                break

    if not db_path or not os.path.exists(db_path):
        abort(404, description="No se encontró el archivo de base de datos.")

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"backup_pacific_{fecha}.db"

    return send_file(
        db_path,
        as_attachment=True,
        download_name=nombre
    )