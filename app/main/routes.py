from datetime import date, timedelta

from flask import render_template
from flask_login import login_required, current_user

from app.main import main_bp
from app.models import (
    Employee,
    Client,
    Invoice,
    Document,
    Incident,
    Payroll,
    Contract
)


@main_bp.route("/")
@login_required
def index():

    hoy = date.today()
    limite = hoy + timedelta(days=30)

    # CONTADORES
    total_empleados = Employee.query.count()
    total_clientes = Client.query.count()
    total_documentos = Document.query.count()
    total_novedades = Incident.query.count()
    total_nomina = Payroll.query.count()
    total_facturas = Invoice.query.count()

    # FACTURAS
    facturas_pendientes = Invoice.query.filter(
        Invoice.estado.in_(["Pendiente", "Enviada", "Vencida"])
    ).count()

    facturas_vencidas = Invoice.query.filter_by(
        estado="Vencida"
    ).count()

    total_cobrar = sum(
        f.total for f in Invoice.query.filter(
            Invoice.estado.in_(["Pendiente", "Enviada", "Vencida"])
        ).all()
    )

    total_vencido = sum(
        f.total for f in Invoice.query.filter_by(
            estado="Vencida"
        ).all()
    )

    # CONTRATOS POR VENCER
    contratos_vencer = Contract.query.filter(
        Contract.fecha_fin <= limite,
        Contract.fecha_fin >= hoy
    ).count()

    # DOCUMENTOS PENDIENTES
    documentos_pendientes = Document.query.filter_by(
        estado="Pendiente"
    ).count()

    return render_template(
        "dashboard.html",
        user=current_user,

        total_empleados=total_empleados,
        total_clientes=total_clientes,
        total_documentos=total_documentos,
        total_novedades=total_novedades,
        total_nomina=total_nomina,
        total_facturas=total_facturas,

        facturas_pendientes=facturas_pendientes,
        facturas_vencidas=facturas_vencidas,

        total_cobrar=total_cobrar,
        total_vencido=total_vencido,

        contratos_vencer=contratos_vencer,
        documentos_pendientes=documentos_pendientes
    )