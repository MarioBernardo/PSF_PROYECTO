from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.inventory import inventory_bp
from app.inventory.forms import InventoryForm
from app.extensions import db
from app.models import Inventory, Post


@inventory_bp.route("/")
@login_required
def list_inventory():
    inventario = Inventory.query.all()
    return render_template("inventory/list.html", inventario=inventario)


@inventory_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_inventory():
    form = InventoryForm()

    form.post_id.choices = [
        (p.id, f"{p.nombre} - {p.ubicacion}")
        for p in Post.query.all()
    ]

    if form.validate_on_submit():
        existe = Inventory.query.filter_by(codigo=form.codigo.data).first()
        if existe:
            flash("El código ya está registrado", "danger")
            return render_template("inventory/form.html", form=form, titulo="Nuevo Equipo")

        equipo = Inventory(
            nombre=form.nombre.data,
            categoria=form.categoria.data,
            codigo=form.codigo.data,
            cantidad=form.cantidad.data,
            estado=form.estado.data,
            observacion=form.observacion.data,
            post_id=form.post_id.data
        )
        db.session.add(equipo)
        db.session.commit()

        flash("Equipo registrado correctamente", "success")
        return redirect(url_for("inventory.list_inventory"))

    return render_template("inventory/form.html", form=form, titulo="Nuevo Equipo")


@inventory_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_inventory(id):
    equipo = Inventory.query.get_or_404(id)
    form = InventoryForm(obj=equipo)

    form.post_id.choices = [
        (p.id, f"{p.nombre} - {p.ubicacion}")
        for p in Post.query.all()
    ]

    if form.validate_on_submit():
        existe = Inventory.query.filter_by(codigo=form.codigo.data).first()
        if existe and existe.id != equipo.id:
            flash("El código ya está registrado en otro equipo", "danger")
            return render_template("inventory/form.html", form=form, titulo="Editar Equipo")

        equipo.nombre = form.nombre.data
        equipo.categoria = form.categoria.data
        equipo.codigo = form.codigo.data
        equipo.cantidad = form.cantidad.data
        equipo.estado = form.estado.data
        equipo.observacion = form.observacion.data
        equipo.post_id = form.post_id.data

        db.session.commit()
        flash("Equipo actualizado correctamente", "success")
        return redirect(url_for("inventory.list_inventory"))

    return render_template("inventory/form.html", form=form, titulo="Editar Equipo")


@inventory_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_inventory(id):
    equipo = Inventory.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()

    flash("Equipo eliminado correctamente", "warning")
    return redirect(url_for("inventory.list_inventory"))