from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.users import users_bp
from app.users.forms import UserForm
from app.extensions import db
from app.models import User
from app.decorators import role_required


@users_bp.route("/")
@login_required
@role_required("admin")
def list_users():
    usuarios = User.query.all()
    return render_template("users/list.html", usuarios=usuarios)


@users_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        existe_username = User.query.filter_by(username=form.username.data).first()
        if existe_username:
            flash("Ese nombre de usuario ya existe", "danger")
            return render_template("users/form.html", form=form, titulo="Nuevo Usuario")

        existe_email = User.query.filter_by(email=form.email.data).first()
        if existe_email:
            flash("Ese correo ya está registrado", "danger")
            return render_template("users/form.html", form=form, titulo="Nuevo Usuario")

        if not form.password.data:
            flash("La contraseña es obligatoria para crear un usuario", "danger")
            return render_template("users/form.html", form=form, titulo="Nuevo Usuario")

        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Usuario creado correctamente", "success")
        return redirect(url_for("users.list_users"))

    return render_template("users/form.html", form=form, titulo="Nuevo Usuario")


@users_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_user(id):
    usuario = User.query.get_or_404(id)
    form = UserForm(obj=usuario)

    if form.validate_on_submit():
        existe_username = User.query.filter_by(username=form.username.data).first()
        if existe_username and existe_username.id != usuario.id:
            flash("Ese nombre de usuario ya existe", "danger")
            return render_template("users/form.html", form=form, titulo="Editar Usuario")

        existe_email = User.query.filter_by(email=form.email.data).first()
        if existe_email and existe_email.id != usuario.id:
            flash("Ese correo ya está registrado", "danger")
            return render_template("users/form.html", form=form, titulo="Editar Usuario")

        usuario.username = form.username.data
        usuario.email = form.email.data
        usuario.role = form.role.data

        if form.password.data:
            usuario.set_password(form.password.data)

        db.session.commit()

        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for("users.list_users"))

    form.password.data = ""
    form.confirm_password.data = ""
    return render_template("users/form.html", form=form, titulo="Editar Usuario")


@users_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_user(id):
    usuario = User.query.get_or_404(id)

    if usuario.username == "admin":
        flash("No se puede eliminar el usuario administrador principal", "danger")
        return redirect(url_for("users.list_users"))

    db.session.delete(usuario)
    db.session.commit()

    flash("Usuario eliminado correctamente", "warning")
    return redirect(url_for("users.list_users"))