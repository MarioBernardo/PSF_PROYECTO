from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app.attendance import attendance_bp
from app.attendance.forms import AttendanceForm
from app.extensions import db
from app.models import Attendance, Employee
from app.decorators import role_required


def cargar_empleados(form):
    form.employee_id.choices = [
        (e.id, f"{e.apellidos} {e.nombres}")
        for e in Employee.query.order_by(
            Employee.apellidos.asc()
        ).all()
    ]


@attendance_bp.route("/")
@login_required
@role_required("admin", "rrhh", "supervisor")
def list_attendance():

    asistencias = Attendance.query.order_by(
        Attendance.id.desc()
    ).all()

    return render_template(
        "attendance/list.html",
        asistencias=asistencias
    )


@attendance_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "rrhh", "supervisor")
def create_attendance():

    form = AttendanceForm()
    cargar_empleados(form)

    if form.validate_on_submit():

        nuevo = Attendance(
            employee_id=form.employee_id.data,
            fecha=form.fecha.data,
            estado=form.estado.data,
            observacion=form.observacion.data
        )

        db.session.add(nuevo)
        db.session.commit()

        flash("Asistencia registrada", "success")
        return redirect(
            url_for("attendance.list_attendance")
        )

    return render_template(
        "attendance/form.html",
        form=form,
        titulo="Nueva Asistencia"
    )


@attendance_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin", "rrhh", "supervisor")
def edit_attendance(id):

    asistencia = Attendance.query.get_or_404(id)

    form = AttendanceForm(obj=asistencia)
    cargar_empleados(form)

    if form.validate_on_submit():

        asistencia.employee_id = form.employee_id.data
        asistencia.fecha = form.fecha.data
        asistencia.estado = form.estado.data
        asistencia.observacion = form.observacion.data

        db.session.commit()

        flash("Asistencia actualizada", "success")
        return redirect(
            url_for("attendance.list_attendance")
        )

    return render_template(
        "attendance/form.html",
        form=form,
        titulo="Editar Asistencia"
    )


@attendance_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_attendance(id):

    asistencia = Attendance.query.get_or_404(id)

    db.session.delete(asistencia)
    db.session.commit()

    flash("Asistencia eliminada", "warning")

    return redirect(
        url_for("attendance.list_attendance")
    )