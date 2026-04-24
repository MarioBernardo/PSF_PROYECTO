from flask import render_template, request
from flask_login import login_required

from app.search import search_bp
from app.models import Employee, Client, Invoice, Document


@search_bp.route("/", methods=["GET"])
@login_required
def global_search():

    q = request.args.get("q", "").strip()

    empleados = []
    clientes = []
    facturas = []
    documentos = []

    if q:

        empleados = Employee.query.filter(
            Employee.nombres.contains(q) |
            Employee.apellidos.contains(q) |
            Employee.cedula.contains(q)
        ).all()

        clientes = Client.query.filter(
            Client.nombre.contains(q) |
            Client.ruc_ci.contains(q)
        ).all()

        facturas = Invoice.query.filter(
            Invoice.numero.contains(q) |
            Invoice.mes.contains(q)
        ).all()

        documentos = Document.query.filter(
            Document.numero.contains(q) |
            Document.titulo.contains(q) |
            Document.tipo.contains(q)
        ).all()

    return render_template(
        "search/results.html",
        q=q,
        empleados=empleados,
        clientes=clientes,
        facturas=facturas,
        documentos=documentos
    )