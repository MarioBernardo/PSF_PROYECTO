from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.delays import delays_bp
from app.delays.forms import DelayForm
from app.extensions import db
from app.models import Delay, Employee, Shift


@delays_bp.route("/")
@login_required
def list_delays():
    atrasos = Delay.query.all()
    return render_template("delays/list.html", atrasos=atrasos)


@delays_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_delay():
    form = DelayForm()

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    form.shift_id.choices = [
        (s.id, f"Turno {s.id} - {s.fecha} - {s.post.nombre}")
        for s in Shift.query.all()
    ]

    if form.validate_on_submit():
        atraso = Delay(
            employee_id=form.employee_id.data,
            shift_id=form.shift_id.data,
            fecha=form.fecha.data,
            minutos=form.minutos.data,
            motivo=form.motivo.data,
            estado=form.estado.data
        )
        db.session.add(atraso)
        db.session.commit()

        flash("Atraso registrado correctamente", "success")
        return redirect(url_for("delays.list_delays"))

    return render_template("delays/form.html", form=form, titulo="Nuevo Atraso")


@delays_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_delay(id):
    atraso = Delay.query.get_or_404(id)
    form = DelayForm(obj=atraso)

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    form.shift_id.choices = [
        (s.id, f"Turno {s.id} - {s.fecha} - {s.post.nombre}")
        for s in Shift.query.all()
    ]

    if form.validate_on_submit():
        atraso.employee_id = form.employee_id.data
        atraso.shift_id = form.shift_id.data
        atraso.fecha = form.fecha.data
        atraso.minutos = form.minutos.data
        atraso.motivo = form.motivo.data
        atraso.estado = form.estado.data

        db.session.commit()
        flash("Atraso actualizado correctamente", "success")
        return redirect(url_for("delays.list_delays"))

    return render_template("delays/form.html", form=form, titulo="Editar Atraso")


@delays_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_delay(id):
    atraso = Delay.query.get_or_404(id)
    db.session.delete(atraso)
    db.session.commit()

    flash("Atraso eliminado correctamente", "warning")
    return redirect(url_for("delays.list_delays"))