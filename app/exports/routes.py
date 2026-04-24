from io import BytesIO
import pandas as pd

from flask import send_file
from flask_login import login_required

from app.exports import exports_bp
from app.models import Employee, Client, Invoice, Attendance, Payroll


def generar_excel(df, nombre):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos")

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=nombre,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@exports_bp.route("/employees")
@login_required
def export_employees():

    data = [{
        "ID": e.id,
        "Nombres": e.nombres,
        "Apellidos": e.apellidos,
        "Cedula": e.cedula,
        "Cargo": e.cargo,
        "Salario": e.salario
    } for e in Employee.query.all()]

    return generar_excel(pd.DataFrame(data), "empleados.xlsx")


@exports_bp.route("/clients")
@login_required
def export_clients():

    data = [{
        "ID": c.id,
        "Cliente": c.nombre,
        "RUC/CI": c.ruc_ci,
        "Telefono": c.telefono
    } for c in Client.query.all()]

    return generar_excel(pd.DataFrame(data), "clientes.xlsx")


@exports_bp.route("/invoices")
@login_required
def export_invoices():

    data = [{
        "ID": f.id,
        "Numero": f.numero,
        "Cliente": f.client.nombre if f.client else "",
        "Tipo": f.tipo_comprobante,
        "Total": f.total,
        "Estado": f.estado
    } for f in Invoice.query.all()]

    return generar_excel(pd.DataFrame(data), "facturas.xlsx")


@exports_bp.route("/attendance")
@login_required
def export_attendance():

    data = [{
        "ID": a.id,
        "Empleado": f"{a.employee.apellidos} {a.employee.nombres}" if a.employee else "",
        "Fecha": a.fecha,
        "Estado": a.estado
    } for a in Attendance.query.all()]

    return generar_excel(pd.DataFrame(data), "asistencia.xlsx")


@exports_bp.route("/payroll")
@login_required
def export_payroll():

    data = [{
        "ID": p.id,
        "Empleado": f"{p.employee.apellidos} {p.employee.nombres}" if p.employee else "",
        "Total": p.total_ingresos,
        "Descuentos": p.total_descuentos,
        "Neto": p.neto_pagar
    } for p in Payroll.query.all()]

    return generar_excel(pd.DataFrame(data), "nomina.xlsx")