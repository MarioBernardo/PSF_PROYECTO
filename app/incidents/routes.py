from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.incidents import incidents_bp
from app.incidents.forms import IncidentForm
from app.extensions import db
from app.models import Incident, Employee, Shift


@incidents_bp.route("/")
@login_required
def list_incidents():
    novedades = Incident.query.all()
    return render_template("incidents/list.html", novedades=novedades)


@incidents_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_incident():
    form = IncidentForm()

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    form.shift_id.choices = [
        (s.id, f"Turno {s.id} - {s.fecha} - {s.post.nombre}")
        for s in Shift.query.all()
    ]

    if form.validate_on_submit():
        novedad = Incident(
            employee_id=form.employee_id.data,
            shift_id=form.shift_id.data,
            tipo=form.tipo.data,
            descripcion=form.descripcion.data,
            fecha=form.fecha.data,
            estado=form.estado.data
        )
        db.session.add(novedad)
        db.session.commit()

        flash("Novedad creada correctamente", "success")
        return redirect(url_for("incidents.list_incidents"))

    return render_template("incidents/form.html", form=form, titulo="Nueva Novedad")


@incidents_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_incident(id):
    novedad = Incident.query.get_or_404(id)
    form = IncidentForm(obj=novedad)

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    form.shift_id.choices = [
        (s.id, f"Turno {s.id} - {s.fecha} - {s.post.nombre}")
        for s in Shift.query.all()
    ]

    if form.validate_on_submit():
        novedad.employee_id = form.employee_id.data
        novedad.shift_id = form.shift_id.data
        novedad.tipo = form.tipo.data
        novedad.descripcion = form.descripcion.data
        novedad.fecha = form.fecha.data
        novedad.estado = form.estado.data

        db.session.commit()
        flash("Novedad actualizada correctamente", "success")
        return redirect(url_for("incidents.list_incidents"))

    return render_template("incidents/form.html", form=form, titulo="Editar Novedad")


@incidents_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_incident(id):
    novedad = Incident.query.get_or_404(id)
    db.session.delete(novedad)
    db.session.commit()

    flash("Novedad eliminada correctamente", "warning")
    return redirect(url_for("incidents.list_incidents"))