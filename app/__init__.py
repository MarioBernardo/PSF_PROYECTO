from flask import Flask, render_template
from app.config import Config
from app.extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.main import main_bp
    from app.auth import auth_bp
    from app.employees import employees_bp
    from app.clients import clients_bp
    from app.contracts import contracts_bp
    from app.assignments import assignments_bp
    from app.posts import posts_bp
    from app.shifts import shifts_bp
    from app.incidents import incidents_bp
    from app.inventory import inventory_bp
    from app.permissions import permissions_bp
    from app.vacations import vacations_bp
    from app.delays import delays_bp
    from app.reports import reports_bp
    from app.users import users_bp
    from app.payroll import payroll_bp
    from app.documents import documents_bp
    from app.invoices import invoices_bp
    from app.search import search_bp
    from app.backup import backup_bp
    from app.attendance import attendance_bp
    from app.exports import exports_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(contracts_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(shifts_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(permissions_bp)
    app.register_blueprint(vacations_bp)
    app.register_blueprint(delays_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(exports_bp)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("403.html"), 403

    return app