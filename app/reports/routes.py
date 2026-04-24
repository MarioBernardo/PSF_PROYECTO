from io import BytesIO
from flask import send_file
from flask_login import login_required
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from app.reports import reports_bp
from app.models import Employee, Client, Contract, Delay, Incident


def cortar_texto(texto, max_chars):
    texto = str(texto) if texto is not None else ""
    if len(texto) > max_chars:
        return texto[:max_chars - 3] + "..."
    return texto


def crear_pdf_tabla(titulo, encabezados, filas, nombre_archivo, anchos):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    pdf.setTitle(titulo)

    def encabezado_pagina():
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(30, height - 35, "PACIFIC SECURITY FORCE CIA. LTDA")

        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(30, height - 58, titulo)

        pdf.line(30, height - 72, width - 30, height - 72)

        y_header = height - 95
        x = 30

        pdf.setFont("Helvetica-Bold", 8)
        for i, encabezado in enumerate(encabezados):
            pdf.drawString(x, y_header, encabezado)
            x += anchos[i]

        pdf.line(30, y_header - 10, width - 30, y_header - 10)

        return y_header - 28

    y = encabezado_pagina()

    pdf.setFont("Helvetica", 7)

    for fila in filas:
        x = 30

        for i, dato in enumerate(fila):
            texto = cortar_texto(dato, 24)

            if encabezados[i] in ["Salario", "Total", "Neto", "Minutos"]:
                pdf.drawRightString(x + anchos[i] - 8, y, texto)
            else:
                pdf.drawString(x, y, texto)

            x += anchos[i]

        y -= 18

        if y < 45:
            pdf.showPage()
            y = encabezado_pagina()
            pdf.setFont("Helvetica", 7)

    pdf.setFont("Helvetica", 7)
    pdf.drawRightString(width - 30, 22, "Generado por Sistema Pacific Security Force")

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype="application/pdf"
    )


@reports_bp.route("/employees")
@login_required
def report_employees():
    empleados = Employee.query.all()

    filas = [
        [
            e.id,
            f"{e.apellidos} {e.nombres}",
            e.cedula,
            e.fecha_ingreso,
            e.cargo,
            e.tipo_puesto,
            f"$ {e.salario:.2f}" if e.salario else "$ 0.00"
        ]
        for e in empleados
    ]

    return crear_pdf_tabla(
        "Reporte de Empleados",
        ["ID", "Empleado", "Cédula", "Ingreso", "Cargo", "Tipo", "Salario"],
        filas,
        "reporte_empleados.pdf",
        [35, 190, 95, 80, 90, 70, 70]
    )


@reports_bp.route("/clients")
@login_required
def report_clients():
    clientes = Client.query.all()

    filas = [
        [
            c.id,
            c.nombre,
            c.ruc_ci,
            c.direccion,
            c.telefono,
            c.correo
        ]
        for c in clientes
    ]

    return crear_pdf_tabla(
        "Reporte de Clientes",
        ["ID", "Cliente", "RUC / CI", "Dirección", "Teléfono", "Correo"],
        filas,
        "reporte_clientes.pdf",
        [35, 160, 100, 210, 90, 180]
    )


@reports_bp.route("/contracts")
@login_required
def report_contracts():
    contratos = Contract.query.all()

    filas = [
        [
            c.id,
            c.cliente.nombre,
            c.tipo_servicio,
            c.fecha_inicio,
            c.fecha_fin,
            c.estado
        ]
        for c in contratos
    ]

    return crear_pdf_tabla(
        "Reporte de Contratos",
        ["ID", "Cliente", "Servicio", "Inicio", "Fin", "Estado"],
        filas,
        "reporte_contratos.pdf",
        [35, 220, 160, 90, 90, 100]
    )


@reports_bp.route("/delays")
@login_required
def report_delays():
    atrasos = Delay.query.all()

    filas = [
        [
            a.id,
            f"{a.employee.apellidos} {a.employee.nombres}",
            a.fecha,
            a.minutos,
            a.motivo,
            a.estado
        ]
        for a in atrasos
    ]

    return crear_pdf_tabla(
        "Reporte de Atrasos",
        ["ID", "Empleado", "Fecha", "Minutos", "Motivo", "Estado"],
        filas,
        "reporte_atrasos.pdf",
        [35, 220, 90, 70, 230, 100]
    )


@reports_bp.route("/incidents")
@login_required
def report_incidents():
    novedades = Incident.query.all()

    filas = [
        [
            n.id,
            f"{n.employee.apellidos} {n.employee.nombres}",
            n.tipo,
            n.fecha,
            n.estado,
            n.descripcion
        ]
        for n in novedades
    ]

    return crear_pdf_tabla(
        "Reporte de Novedades",
        ["ID", "Empleado", "Tipo", "Fecha", "Estado", "Descripción"],
        filas,
        "reporte_novedades.pdf",
        [35, 220, 100, 90, 90, 250]
    )