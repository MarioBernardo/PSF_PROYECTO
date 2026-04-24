from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.employees import employees_bp
from app.extensions import db
from app.models import Employee
from app.employees.forms import EmployeeForm
from app.decorators import role_required


@employees_bp.route("/")
@login_required
@role_required("admin", "rrhh", "supervisor")
def list_employees():
    empleados = Employee.query.all()
    return render_template("employees/list.html", empleados=empleados)


@employees_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "rrhh")
def create_employee():
    form = EmployeeForm()

    if form.validate_on_submit():
        existe = Employee.query.filter_by(cedula=form.cedula.data).first()
        if existe:
            flash("La cédula ya está registrada", "danger")
            return render_template("employees/form.html", form=form, titulo="Nuevo Empleado")

        emp = Employee(
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            cedula=form.cedula.data,
            fecha_ingreso=form.fecha_ingreso.data,
            tipo_puesto=form.tipo_puesto.data,
            cargo=form.cargo.data,
            salario=form.salario.data
        )

        db.session.add(emp)
        db.session.commit()

        flash("Empleado creado correctamente", "success")
        return redirect(url_for("employees.list_employees"))

    return render_template("employees/form.html", form=form, titulo="Nuevo Empleado")


@employees_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin", "rrhh")
def edit_employee(id):
    empleado = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=empleado)

    if form.validate_on_submit():
        existe = Employee.query.filter_by(cedula=form.cedula.data).first()
        if existe and existe.id != empleado.id:
            flash("La cédula ya está registrada en otro empleado", "danger")
            return render_template("employees/form.html", form=form, titulo="Editar Empleado")

        empleado.nombres = form.nombres.data
        empleado.apellidos = form.apellidos.data
        empleado.cedula = form.cedula.data
        empleado.fecha_ingreso = form.fecha_ingreso.data
        empleado.tipo_puesto = form.tipo_puesto.data
        empleado.cargo = form.cargo.data
        empleado.salario = form.salario.data

        db.session.commit()

        flash("Empleado actualizado correctamente", "success")
        return redirect(url_for("employees.list_employees"))

    return render_template("employees/form.html", form=form, titulo="Editar Empleado")


@employees_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_employee(id):
    empleado = Employee.query.get_or_404(id)

    db.session.delete(empleado)
    db.session.commit()

    flash("Empleado eliminado correctamente", "warning")
    return redirect(url_for("employees.list_employees"))