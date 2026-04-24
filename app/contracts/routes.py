from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.contracts import contracts_bp
from app.extensions import db
from app.models import Contract, Client
from app.contracts.forms import ContractForm


@contracts_bp.route("/")
@login_required
def list_contracts():
    contratos = Contract.query.all()
    return render_template("contracts/list.html", contratos=contratos)


@contracts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_contract():
    form = ContractForm()
    form.cliente_id.choices = [(c.id, c.nombre) for c in Client.query.all()]

    if form.validate_on_submit():
        if form.fecha_fin.data < form.fecha_inicio.data:
            flash("La fecha fin no puede ser menor que la fecha inicio", "danger")
            return render_template("contracts/form.html", form=form, titulo="Nuevo Contrato")

        contrato = Contract(
            cliente_id=form.cliente_id.data,
            tipo_servicio=form.tipo_servicio.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            estado=form.estado.data
        )
        db.session.add(contrato)
        db.session.commit()

        flash("Contrato creado correctamente", "success")
        return redirect(url_for("contracts.list_contracts"))

    return render_template("contracts/form.html", form=form, titulo="Nuevo Contrato")


@contracts_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_contract(id):
    contrato = Contract.query.get_or_404(id)
    form = ContractForm(obj=contrato)
    form.cliente_id.choices = [(c.id, c.nombre) for c in Client.query.all()]

    if form.validate_on_submit():
        if form.fecha_fin.data < form.fecha_inicio.data:
            flash("La fecha fin no puede ser menor que la fecha inicio", "danger")
            return render_template("contracts/form.html", form=form, titulo="Editar Contrato")

        contrato.cliente_id = form.cliente_id.data
        contrato.tipo_servicio = form.tipo_servicio.data
        contrato.fecha_inicio = form.fecha_inicio.data
        contrato.fecha_fin = form.fecha_fin.data
        contrato.estado = form.estado.data

        db.session.commit()
        flash("Contrato actualizado correctamente", "success")
        return redirect(url_for("contracts.list_contracts"))

    return render_template("contracts/form.html", form=form, titulo="Editar Contrato")


@contracts_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_contract(id):
    contrato = Contract.query.get_or_404(id)
    db.session.delete(contrato)
    db.session.commit()

    flash("Contrato eliminado correctamente", "warning")
    return redirect(url_for("contracts.list_contracts"))