from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.decorators import role_required
from app.clients import clients_bp
from app.extensions import db
from app.models import Client
from app.clients.forms import ClientForm


@clients_bp.route("/")
@login_required
@role_required("admin", "supervisor")
def list_clients():
    clientes = Client.query.all()
    return render_template("clients/list.html", clientes=clientes)


@clients_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "supervisor")
def create_client():
    form = ClientForm()

    if form.validate_on_submit():
        cliente = Client(
            nombre=form.nombre.data,
            ruc_ci=form.ruc_ci.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            correo=form.correo.data
        )

        db.session.add(cliente)
        db.session.commit()

        flash("Cliente creado correctamente", "success")
        return redirect(url_for("clients.list_clients"))

    return render_template("clients/form.html", form=form, titulo="Nuevo Cliente")


@clients_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin", "supervisor")
def edit_client(id):
    cliente = Client.query.get_or_404(id)
    form = ClientForm(obj=cliente)

    if form.validate_on_submit():
        cliente.nombre = form.nombre.data
        cliente.ruc_ci = form.ruc_ci.data
        cliente.direccion = form.direccion.data
        cliente.telefono = form.telefono.data
        cliente.correo = form.correo.data

        db.session.commit()

        flash("Cliente actualizado correctamente", "success")
        return redirect(url_for("clients.list_clients"))

    return render_template("clients/form.html", form=form, titulo="Editar Cliente")


@clients_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_client(id):
    cliente = Client.query.get_or_404(id)

    db.session.delete(cliente)
    db.session.commit()

    flash("Cliente eliminado correctamente", "warning")
    return redirect(url_for("clients.list_clients"))