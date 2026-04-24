from datetime import date
from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app.invoices import invoices_bp
from app.invoices.forms import InvoiceForm
from app.extensions import db
from app.models import Invoice, Client
from app.decorators import role_required


def cargar_clientes(form):
    form.client_id.choices = [
        (c.id, c.nombre)
        for c in Client.query.order_by(Client.nombre.asc()).all()
    ]


def calcular_valores(form):
    subtotal = form.subtotal.data or 0

    if form.tipo_comprobante.data == "Factura":
        iva = subtotal * 0.15
    else:
        iva = 0

    total = subtotal + iva

    return round(subtotal, 2), round(iva, 2), round(total, 2)


def dias_vencidos(factura):
    if factura.estado == "Pagada":
        return 0

    if not factura.fecha_vencimiento:
        return 0

    hoy = date.today()

    if hoy > factura.fecha_vencimiento:
        return (hoy - factura.fecha_vencimiento).days

    return 0


def actualizar_estado_vencida(factura):
    if factura.estado in ["Pagada", "Anulada"]:
        return

    if factura.fecha_vencimiento and date.today() > factura.fecha_vencimiento:
        factura.estado = "Vencida"


@invoices_bp.route("/")
@login_required
@role_required("admin", "rrhh", "supervisor")
def list_invoices():
    facturas = Invoice.query.order_by(Invoice.id.desc()).all()

    for f in facturas:
        actualizar_estado_vencida(f)

    db.session.commit()

    total_cobrar = sum(
        f.total for f in facturas
        if f.estado in ["Pendiente", "Enviada", "Vencida"]
    )

    total_vencido = sum(
        f.total for f in facturas
        if f.estado == "Vencida"
    )

    total_pagado = sum(
        f.total for f in facturas
        if f.estado == "Pagada"
    )

    return render_template(
        "invoices/list.html",
        facturas=facturas,
        total_cobrar=total_cobrar,
        total_vencido=total_vencido,
        total_pagado=total_pagado,
        dias_vencidos=dias_vencidos
    )


@invoices_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "rrhh")
def create_invoice():
    form = InvoiceForm()
    cargar_clientes(form)

    if form.validate_on_submit():
        subtotal, iva, total = calcular_valores(form)

        factura = Invoice(
            client_id=form.client_id.data,
            numero=form.numero.data,
            tipo_comprobante=form.tipo_comprobante.data,
            mes=form.mes.data,
            fecha=form.fecha.data,
            fecha_vencimiento=form.fecha_vencimiento.data,
            subtotal=subtotal,
            iva=iva,
            total=total,
            estado=form.estado.data,
            observacion=form.observacion.data
        )

        actualizar_estado_vencida(factura)

        db.session.add(factura)
        db.session.commit()

        flash("Comprobante registrado correctamente", "success")
        return redirect(url_for("invoices.list_invoices"))

    return render_template("invoices/form.html", form=form, titulo="Nuevo Comprobante")


@invoices_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin", "rrhh")
def edit_invoice(id):
    factura = Invoice.query.get_or_404(id)
    form = InvoiceForm(obj=factura)
    cargar_clientes(form)

    if form.validate_on_submit():
        subtotal, iva, total = calcular_valores(form)

        factura.client_id = form.client_id.data
        factura.numero = form.numero.data
        factura.tipo_comprobante = form.tipo_comprobante.data
        factura.mes = form.mes.data
        factura.fecha = form.fecha.data
        factura.fecha_vencimiento = form.fecha_vencimiento.data
        factura.subtotal = subtotal
        factura.iva = iva
        factura.total = total
        factura.estado = form.estado.data
        factura.observacion = form.observacion.data

        actualizar_estado_vencida(factura)

        db.session.commit()

        flash("Comprobante actualizado correctamente", "success")
        return redirect(url_for("invoices.list_invoices"))

    return render_template("invoices/form.html", form=form, titulo="Editar Comprobante")


@invoices_bp.route("/mark-paid/<int:id>", methods=["POST"])
@login_required
@role_required("admin", "rrhh")
def mark_paid(id):
    factura = Invoice.query.get_or_404(id)
    factura.estado = "Pagada"
    db.session.commit()

    flash("Comprobante marcado como pagado", "success")
    return redirect(url_for("invoices.list_invoices"))


@invoices_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_invoice(id):
    factura = Invoice.query.get_or_404(id)

    db.session.delete(factura)
    db.session.commit()

    flash("Comprobante eliminado correctamente", "warning")
    return redirect(url_for("invoices.list_invoices"))