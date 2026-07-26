from io import BytesIO
from datetime import date
from flask import render_template, redirect, url_for, flash, send_file
from flask_login import login_required
from reportlab.pdfgen import canvas

from app.payroll import payroll_bp
from app.payroll.forms import PayrollForm
from app.extensions import db
from app.models import Payroll, Employee
from app.decorators import role_required


def calcular_meses_trabajados(fecha_ingreso):
    if not fecha_ingreso:
        return 0

    hoy = date.today()
    meses = (hoy.year - fecha_ingreso.year) * 12 + (hoy.month - fecha_ingreso.month)

    if hoy.day < fecha_ingreso.day:
        meses -= 1

    return max(meses, 0)


def generar_numero_rol():
    ultimo = Payroll.query.order_by(Payroll.id.desc()).first()
    siguiente = ultimo.id + 1 if ultimo else 1
    return f"{str(siguiente).zfill(4)}"


def calcular_rol(form, empleado):
    tipo_pago = form.tipo_pago.data
    base_iess = form.base_iess.data

    sueldo_basico = form.sueldo_basico.data or 0
    horas_extras = form.horas_extras.data or 0
    otros_ingresos = form.otros_ingresos.data or 0

    prestamo_quirografario = form.prestamo_quirografario.data or 0
    anticipo_empresa = form.anticipo_empresa.data or 0
    multas = form.multas.data or 0
    otros_descuentos = form.otros_descuentos.data or 0

    turnos_realizados = form.turnos_realizados.data or 0
    valor_turno = form.valor_turno.data or 0

    if tipo_pago == "turno":
        base_iess = "no_aplica"
        sueldo_basico = 0
        horas_extras = 0
        decimo_tercero = 0
        decimo_cuarto = 0
        aporte_iess = 0
        fondos_reserva = 0
        otros_ingresos = turnos_realizados * valor_turno
    else:
        decimo_tercero = (sueldo_basico + horas_extras) / 12
        decimo_cuarto = sueldo_basico / 12

        if base_iess == "total":
            aporte_iess = (sueldo_basico + horas_extras) * 0.0945
        else:
            aporte_iess = sueldo_basico * 0.0945

        meses = calcular_meses_trabajados(empleado.fecha_ingreso)

        if meses >= 13:
            fondos_reserva = (sueldo_basico + horas_extras) * 0.0833
        else:
            fondos_reserva = 0

    total_ingresos = (
        sueldo_basico +
        horas_extras +
        decimo_tercero +
        decimo_cuarto +
        fondos_reserva +
        otros_ingresos
    )

    total_descuentos = (
        aporte_iess +
        prestamo_quirografario +
        anticipo_empresa +
        multas +
        otros_descuentos
    )

    neto_pagar = total_ingresos - total_descuentos

    return {
        "tipo_pago": tipo_pago,
        "base_iess": base_iess,
        "turnos_realizados": turnos_realizados,
        "valor_turno": valor_turno,
        "sueldo_basico": round(sueldo_basico, 2),
        "horas_extras": round(horas_extras, 2),
        "decimo_tercero": round(decimo_tercero, 2),
        "decimo_cuarto": round(decimo_cuarto, 2),
        "fondos_reserva": round(fondos_reserva, 2),
        "otros_ingresos": round(otros_ingresos, 2),
        "aporte_iess": round(aporte_iess, 2),
        "prestamo_quirografario": round(prestamo_quirografario, 2),
        "anticipo_empresa": round(anticipo_empresa, 2),
        "multas": round(multas, 2),
        "otros_descuentos": round(otros_descuentos, 2),
        "total_ingresos": round(total_ingresos, 2),
        "total_descuentos": round(total_descuentos, 2),
        "neto_pagar": round(neto_pagar, 2),
    }


@payroll_bp.route("/")
@login_required
@role_required("admin", "rrhh")
def list_payroll():
    roles = Payroll.query.order_by(Payroll.id.desc()).all()
    return render_template("payroll/list.html", roles=roles)


@payroll_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "rrhh")
def create_payroll():
    form = PayrollForm()

    empleados = Employee.query.order_by(Employee.apellidos.asc()).all()
    form.employee_id.choices = [
        (e.id, f"{e.apellidos} {e.nombres} - {e.cedula}")
        for e in empleados
    ]

    if form.validate_on_submit():
        empleado = Employee.query.get(form.employee_id.data)

        if not empleado:
            flash("Empleado no encontrado", "danger")
            return redirect(url_for("payroll.create_payroll"))

        datos = calcular_rol(form, empleado)
        numero_rol = generar_numero_rol()

        nuevo = Payroll(
            numero_rol=numero_rol,
            employee_id=empleado.id,
            mes=form.mes.data,
            anio=form.anio.data,
            **datos
        )

        db.session.add(nuevo)
        db.session.commit()

        flash(f"Rol creado correctamente. No. PSF-{numero_rol}", "success")
        return redirect(url_for("payroll.list_payroll"))

    return render_template("payroll/form.html", form=form, titulo="Nuevo Rol de Pago")


@payroll_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin", "rrhh")
def edit_payroll(id):
    rol = Payroll.query.get_or_404(id)
    form = PayrollForm(obj=rol)

    empleados = Employee.query.order_by(Employee.apellidos.asc()).all()
    form.employee_id.choices = [
        (e.id, f"{e.apellidos} {e.nombres} - {e.cedula}")
        for e in empleados
    ]

    if form.validate_on_submit():
        empleado = Employee.query.get(form.employee_id.data)

        if not empleado:
            flash("Empleado no encontrado", "danger")
            return redirect(url_for("payroll.edit_payroll", id=id))

        datos = calcular_rol(form, empleado)

        rol.employee_id = empleado.id
        rol.mes = form.mes.data
        rol.anio = form.anio.data

        for campo, valor in datos.items():
            setattr(rol, campo, valor)

        db.session.commit()

        flash("Rol actualizado correctamente", "success")
        return redirect(url_for("payroll.list_payroll"))

    return render_template("payroll/form.html", form=form, titulo="Editar Rol de Pago")


@payroll_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_payroll(id):
    rol = Payroll.query.get_or_404(id)
    db.session.delete(rol)
    db.session.commit()

    flash("Rol eliminado correctamente", "warning")
    return redirect(url_for("payroll.list_payroll"))


@payroll_bp.route("/pdf/<int:id>")
@login_required
@role_required("admin", "rrhh")
def payroll_pdf(id):
    rol = Payroll.query.get_or_404(id)
    empleado = rol.employee

    buffer = BytesIO()

    width = 842
    height = 420
    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    pdf.setTitle(f"Rol_PSF_{rol.numero_rol}")

    pdf.rect(20, 20, 802, 380)

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(421, 382, "PACIFIC SECURITY FORCE CIA. LTDA")

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(35, 360, "ROL DE PAGOS INDIVIDUAL")
    pdf.drawString(650, 360, f"No. PSF-{rol.numero_rol}")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(35, 338, "MES DE:")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(90, 338, f"{rol.mes} {rol.anio}")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(35, 315, "EMPLEADO:")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(130, 315, f"{empleado.apellidos} {empleado.nombres}")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(35, 295, "CEDULA:")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(130, 295, empleado.cedula)

    pdf.setFont("Helvetica", 10)
    pdf.drawString(35, 275, "CARGO:")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(130, 275, empleado.cargo)

    pdf.setFont("Helvetica", 10)
    pdf.drawString(430, 275, "TIPO PAGO:")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(520, 275, rol.tipo_pago.upper())

    pdf.line(20, 260, 822, 260)
    pdf.line(421, 260, 421, 105)

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(220, 245, "INGRESOS")
    pdf.drawCentredString(620, 245, "DESCUENTOS")

    pdf.setFont("Helvetica", 9)
    y = 225

    if rol.tipo_pago == "turno":
        ingresos = [
            (f"Pago por Turnos ({rol.turnos_realizados} x ${rol.valor_turno:.2f})", rol.otros_ingresos)
        ]
    else:
        ingresos = [
            ("Sueldo Básico", rol.sueldo_basico),
            ("Horas Extras", rol.horas_extras),
            ("Décimo Tercer Sueldo", rol.decimo_tercero),
            ("Décimo Cuarto Sueldo", rol.decimo_cuarto),
            ("Fondos de Reserva", rol.fondos_reserva),
            ("Otros Ingresos", rol.otros_ingresos),
        ]

    for concepto, valor in ingresos:
        pdf.drawString(40, y, concepto)
        pdf.drawRightString(390, y, f"$ {valor:,.2f}")
        y -= 18

    y2 = 225

    if rol.tipo_pago == "turno":
        descuentos = [
            ("Anticipo Empresa", rol.anticipo_empresa),
            ("Multas", rol.multas),
            ("Otros Descuentos", rol.otros_descuentos),
        ]
    else:
        descuentos = [
            ("Aporte IESS", rol.aporte_iess),
            ("Préstamo Quirografario IESS", rol.prestamo_quirografario),
            ("Anticipo Empresa", rol.anticipo_empresa),
            ("Multas", rol.multas),
            ("Otros Descuentos", rol.otros_descuentos),
        ]

    for concepto, valor in descuentos:
        pdf.drawString(440, y2, concepto)
        pdf.drawRightString(790, y2, f"$ {valor:,.2f}")
        y2 -= 18

    pdf.line(20, 105, 822, 105)

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, 88, "TOTAL INGRESOS")
    pdf.drawRightString(390, 88, f"$ {rol.total_ingresos:,.2f}")

    pdf.drawString(440, 88, "TOTAL DESCUENTOS")
    pdf.drawRightString(790, 88, f"$ {rol.total_descuentos:,.2f}")

    pdf.line(20, 72, 822, 72)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 52, "NETO A PAGAR")
    pdf.drawRightString(390, 52, f"$ {rol.neto_pagar:,.2f}")

    pdf.setFont("Helvetica", 9)
    pdf.line(520, 48, 760, 48)
    pdf.drawCentredString(640, 35, "RECIBÍ CONFORME")
    pdf.drawString(555, 22, "C.I.")
    pdf.line(585, 22, 735, 22)

    pdf.save()
    buffer.seek(0)

    return send_file(
    buffer,
    as_attachment=True,
    download_name=(
        f"{empleado.apellidos.upper()} "
        f"{empleado.nombres.upper()} - "
        f"{rol.mes.upper()} {rol.anio}.pdf"
    ),
    mimetype="application/pdf"
)