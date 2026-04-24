from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.permissions import permissions_bp
from app.permissions.forms import PermissionForm
from app.extensions import db
from app.models import Permission, Employee


@permissions_bp.route("/")
@login_required
def list_permissions():
    permisos = Permission.query.all()
    return render_template("permissions/list.html", permisos=permisos)


@permissions_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_permission():
    form = PermissionForm()

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    if form.validate_on_submit():
        if form.fecha_fin.data < form.fecha_inicio.data:
            flash("La fecha fin no puede ser menor que la fecha inicio", "danger")
            return render_template("permissions/form.html", form=form, titulo="Nuevo Permiso")

        permiso = Permission(
            employee_id=form.employee_id.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            motivo=form.motivo.data,
            descripcion=form.descripcion.data,
            estado=form.estado.data
        )
        db.session.add(permiso)
        db.session.commit()

        flash("Permiso registrado correctamente", "success")
        return redirect(url_for("permissions.list_permissions"))

    return render_template("permissions/form.html", form=form, titulo="Nuevo Permiso")


@permissions_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_permission(id):
    permiso = Permission.query.get_or_404(id)
    form = PermissionForm(obj=permiso)

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    if form.validate_on_submit():
        if form.fecha_fin.data < form.fecha_inicio.data:
            flash("La fecha fin no puede ser menor que la fecha inicio", "danger")
            return render_template("permissions/form.html", form=form, titulo="Editar Permiso")

        permiso.employee_id = form.employee_id.data
        permiso.fecha_inicio = form.fecha_inicio.data
        permiso.fecha_fin = form.fecha_fin.data
        permiso.motivo = form.motivo.data
        permiso.descripcion = form.descripcion.data
        permiso.estado = form.estado.data

        db.session.commit()
        flash("Permiso actualizado correctamente", "success")
        return redirect(url_for("permissions.list_permissions"))

    return render_template("permissions/form.html", form=form, titulo="Editar Permiso")


@permissions_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_permission(id):
    permiso = Permission.query.get_or_404(id)
    db.session.delete(permiso)
    db.session.commit()

    flash("Permiso eliminado correctamente", "warning")
    return redirect(url_for("permissions.list_permissions"))