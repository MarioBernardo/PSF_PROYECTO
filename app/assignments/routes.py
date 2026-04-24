from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.assignments import assignments_bp
from app.assignments.forms import AssignmentForm
from app.extensions import db
from app.models import ContractEmployee, Contract, Employee


@assignments_bp.route("/")
@login_required
def list_assignments():
    asignaciones = ContractEmployee.query.all()
    return render_template("assignments/list.html", asignaciones=asignaciones)


@assignments_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_assignment():
    form = AssignmentForm()

    form.contract_id.choices = [
        (c.id, f"{c.id} - {c.cliente.nombre} - {c.tipo_servicio}")
        for c in Contract.query.all()
    ]

    form.employee_id.choices = [
        (e.id, f"{e.nombres} {e.apellidos} - {e.cedula}")
        for e in Employee.query.all()
    ]

    if form.validate_on_submit():
        existe = ContractEmployee.query.filter_by(
            contract_id=form.contract_id.data,
            employee_id=form.employee_id.data
        ).first()

        if existe:
            flash("Ese empleado ya está asignado a ese contrato", "danger")
            return render_template("assignments/form.html", form=form, titulo="Nueva Asignación")

        asignacion = ContractEmployee(
            contract_id=form.contract_id.data,
            employee_id=form.employee_id.data
        )
        db.session.add(asignacion)
        db.session.commit()

        flash("Empleado asignado correctamente", "success")
        return redirect(url_for("assignments.list_assignments"))

    return render_template("assignments/form.html", form=form, titulo="Nueva Asignación")


@assignments_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_assignment(id):
    asignacion = ContractEmployee.query.get_or_404(id)
    db.session.delete(asignacion)
    db.session.commit()

    flash("Asignación eliminada correctamente", "warning")
    return redirect(url_for("assignments.list_assignments"))