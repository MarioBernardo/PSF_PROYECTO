from datetime import date, datetime
from flask import Flask, render_template
from app.config import Config
from app.extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.models import (
        User,
        Employee,
        Client,
        Contract,
        Invoice,
        Payroll,
        Vacation,
    )

    @app.context_processor
    def inject_dashboard_metrics():
        today = date.today()
        month_label = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }[today.month]

        hour = datetime.now().hour
        if hour < 12:
            greeting = "Buenos días"
        elif hour < 19:
            greeting = "Buenas tardes"
        else:
            greeting = "Buenas noches"

        facturas_mes = [
            invoice for invoice in Invoice.query.all()
            if invoice.fecha and invoice.fecha.year == today.year and invoice.fecha.month == today.month
        ]
        facturacion_mes = sum(invoice.total for invoice in facturas_mes)

        roles_mes = [
            payroll for payroll in Payroll.query.all()
            if payroll.anio == today.year and payroll.mes == month_label
        ]
        gasto_nomina_mes = sum(payroll.neto_pagar for payroll in roles_mes)
        ganancia_mes = round(facturacion_mes - gasto_nomina_mes, 2)
        ganancia_acumulada = round(
            sum(invoice.total for invoice in Invoice.query.all()) - sum(payroll.neto_pagar for payroll in Payroll.query.all()),
            2,
        )

        facturas_pendientes = Invoice.query.filter(
            Invoice.estado.in_(["Pendiente", "Enviada", "Vencida"])
        ).count()
        clientes_activos = Client.query.count()
        contratos_activos = Contract.query.filter_by(estado="Activo").count()
        empleados_activos = Employee.query.count()
        roles_generados = len(roles_mes)

        ultimo_rol = Payroll.query.order_by(Payroll.id.desc()).first()
        ultima_factura = Invoice.query.order_by(Invoice.id.desc()).first()
        ultimo_cliente = Client.query.order_by(Client.id.desc()).first()
        ultimo_contrato = Contract.query.order_by(Contract.id.desc()).first()

        actividad_reciente = []
        if ultimo_rol:
            actividad_reciente.append({
                "title": "Nuevo rol generado",
                "detail": f"{ultimo_rol.employee.apellidos} {ultimo_rol.employee.nombres}",
                "meta": f"PSF-{ultimo_rol.numero_rol}",
            })
        if ultima_factura:
            actividad_reciente.append({
                "title": "Factura creada",
                "detail": f"{ultima_factura.numero} · {ultima_factura.client.nombre if ultima_factura.client else '-'}",
                "meta": ultima_factura.estado,
            })
        if ultimo_cliente:
            actividad_reciente.append({
                "title": "Cliente registrado",
                "detail": ultimo_cliente.nombre,
                "meta": f"RUC/CI {ultimo_cliente.ruc_ci or '-'}",
            })
        if ultimo_contrato:
            actividad_reciente.append({
                "title": "Contrato actualizado",
                "detail": f"{ultimo_contrato.tipo_servicio or 'Servicio'} · {ultimo_contrato.estado}",
                "meta": ultimo_contrato.cliente.nombre if ultimo_contrato.cliente else "Cliente",
            })

        facturas_vencidas = Invoice.query.filter_by(estado="Vencida").count()
        limite = date.today().replace(day=28)
        contratos_por_vencer = Contract.query.filter(
            Contract.fecha_fin.isnot(None),
            Contract.fecha_fin >= date.today(),
            Contract.fecha_fin <= limite
        ).count()

        vacaciones_pendientes = Vacation.query.filter_by(estado="Programada").count()

        upcoming_events = []
        for invoice in Invoice.query.filter(Invoice.fecha_vencimiento.isnot(None)).order_by(Invoice.fecha_vencimiento.asc()).all():
            if invoice.fecha_vencimiento and invoice.fecha_vencimiento >= today:
                upcoming_events.append({
                    "date": invoice.fecha_vencimiento.strftime("%d %b"),
                    "title": f"Factura vence · {invoice.numero}",
                    "detail": invoice.client.nombre if invoice.client else "Cliente",
                })
                if len(upcoming_events) == 3:
                    break

        for contract in Contract.query.filter(Contract.fecha_fin.isnot(None)).order_by(Contract.fecha_fin.asc()).all():
            if contract.fecha_fin and contract.fecha_fin >= today and contract.estado == "Activo":
                upcoming_events.append({
                    "date": contract.fecha_fin.strftime("%d %b"),
                    "title": f"Contrato vence · {contract.tipo_servicio or 'Servicio'}",
                    "detail": contract.cliente.nombre if contract.cliente else "Cliente",
                })
                if len(upcoming_events) == 6:
                    break

        for vacation in Vacation.query.filter_by(estado="Programada").order_by(Vacation.fecha_inicio.asc()).all():
            if vacation.fecha_inicio and vacation.fecha_inicio >= today:
                upcoming_events.append({
                    "date": vacation.fecha_inicio.strftime("%d %b"),
                    "title": "Vacación programada",
                    "detail": f"{vacation.employee.apellidos} {vacation.employee.nombres}",
                })
                if len(upcoming_events) == 8:
                    break

        for shift in []:
            pass

        alertas = []
        if facturas_vencidas:
            alertas.append({
                "title": "Facturas vencidas",
                "detail": f"{facturas_vencidas} comprobante(s) requieren seguimiento",
                "meta": "Prioridad alta",
            })
        if contratos_por_vencer:
            alertas.append({
                "title": "Contratos próximos a vencer",
                "detail": f"{contratos_por_vencer} contrato(s) en los próximos 30 días",
                "meta": "Revisión recomendada",
            })
        if vacaciones_pendientes:
            alertas.append({
                "title": "Vacaciones pendientes",
                "detail": f"{vacaciones_pendientes} solicitud(es) programadas",
                "meta": "Planificación",
            })

        day_summary = f"Hoy tienes {len(alertas)} alertas y {len(actividad_reciente)} movimientos recientes."

        return {
            "dashboard_metrics": {
                "facturacion_mes": round(facturacion_mes, 2),
                "gasto_nomina_mes": round(gasto_nomina_mes, 2),
                "ganancia_mes": round(ganancia_mes, 2),
                "ganancia_acumulada": round(ganancia_acumulada, 2),
                "facturas_pendientes": facturas_pendientes,
                "clientes_activos": clientes_activos,
                "contratos_activos": contratos_activos,
                "empleados_activos": empleados_activos,
                "roles_generados": roles_generados,
                "actividad_reciente": actividad_reciente,
                "alertas": alertas,
                "period_label": month_label,
                "greeting": greeting,
                "day_summary": day_summary,
                "upcoming_events": upcoming_events[:4],
            }
        }

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