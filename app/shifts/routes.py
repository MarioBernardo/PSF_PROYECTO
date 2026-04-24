from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.shifts import shifts_bp
from app.shifts.forms import ShiftForm
from app.extensions import db
from app.models import Shift, Employee, Post


@shifts_bp.route("/")
@login_required
def list_shifts():
    turnos = Shift.query.all()
    return render_template("shifts/list.html", turnos=turnos)


@shifts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_shift():
    form = ShiftForm()

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    form.post_id.choices = [
        (p.id, f"{p.nombre} - {p.ubicacion}")
        for p in Post.query.all()
    ]

    if form.validate_on_submit():
        turno = Shift(
            employee_id=form.employee_id.data,
            post_id=form.post_id.data,
            fecha=form.fecha.data,
            tipo_turno=form.tipo_turno.data,
            estado=form.estado.data
        )

        db.session.add(turno)
        db.session.commit()

        flash("Turno creado correctamente", "success")
        return redirect(url_for("shifts.list_shifts"))

    return render_template("shifts/form.html", form=form, titulo="Nuevo Turno")


@shifts_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_shift(id):
    turno = Shift.query.get_or_404(id)
    form = ShiftForm(obj=turno)

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    form.post_id.choices = [
        (p.id, f"{p.nombre} - {p.ubicacion}")
        for p in Post.query.all()
    ]

    if form.validate_on_submit():
        turno.employee_id = form.employee_id.data
        turno.post_id = form.post_id.data
        turno.fecha = form.fecha.data
        turno.tipo_turno = form.tipo_turno.data
        turno.estado = form.estado.data

        db.session.commit()

        flash("Turno actualizado correctamente", "success")
        return redirect(url_for("shifts.list_shifts"))

    return render_template("shifts/form.html", form=form, titulo="Editar Turno")


@shifts_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_shift(id):
    turno = Shift.query.get_or_404(id)

    db.session.delete(turno)
    db.session.commit()

    flash("Turno eliminado correctamente", "warning")
    return redirect(url_for("shifts.list_shifts"))