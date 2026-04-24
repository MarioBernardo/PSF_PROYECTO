from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.vacations import vacations_bp
from app.vacations.forms import VacationForm
from app.extensions import db
from app.models import Vacation, Employee


@vacations_bp.route("/")
@login_required
def list_vacations():
    vacaciones = Vacation.query.all()
    return render_template("vacations/list.html", vacaciones=vacaciones)


@vacations_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_vacation():
    form = VacationForm()

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    if form.validate_on_submit():
        if form.fecha_fin.data < form.fecha_inicio.data:
            flash("La fecha fin no puede ser menor que la fecha inicio", "danger")
            return render_template("vacations/form.html", form=form, titulo="Nueva Vacación")

        vacacion = Vacation(
            employee_id=form.employee_id.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            dias=form.dias.data,
            observacion=form.observacion.data,
            estado=form.estado.data
        )
        db.session.add(vacacion)
        db.session.commit()

        flash("Vacación registrada correctamente", "success")
        return redirect(url_for("vacations.list_vacations"))

    return render_template("vacations/form.html", form=form, titulo="Nueva Vacación")


@vacations_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_vacation(id):
    vacacion = Vacation.query.get_or_404(id)
    form = VacationForm(obj=vacacion)

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    if form.validate_on_submit():
        if form.fecha_fin.data < form.fecha_inicio.data:
            flash("La fecha fin no puede ser menor que la fecha inicio", "danger")
            return render_template("vacations/form.html", form=form, titulo="Editar Vacación")

        vacacion.employee_id = form.employee_id.data
        vacacion.fecha_inicio = form.fecha_inicio.data
        vacacion.fecha_fin = form.fecha_fin.data
        vacacion.dias = form.dias.data
        vacacion.observacion = form.observacion.data
        vacacion.estado = form.estado.data

        db.session.commit()
        flash("Vacación actualizada correctamente", "success")
        return redirect(url_for("vacations.list_vacations"))

    return render_template("vacations/form.html", form=form, titulo="Editar Vacación")


@vacations_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_vacation(id):
    vacacion = Vacation.query.get_or_404(id)
    db.session.delete(vacacion)
    db.session.commit()

    flash("Vacación eliminada correctamente", "warning")
    return redirect(url_for("vacations.list_vacations"))