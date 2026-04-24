from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.posts import posts_bp
from app.posts.forms import PostForm
from app.extensions import db
from app.models import Post, Contract


@posts_bp.route("/")
@login_required
def list_posts():
    puestos = Post.query.all()
    return render_template("posts/list.html", puestos=puestos)


@posts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    form.contract_id.choices = [
        (c.id, f"{c.id} - {c.cliente.nombre} - {c.tipo_servicio}")
        for c in Contract.query.all()
    ]

    if form.validate_on_submit():
        puesto = Post(
            nombre=form.nombre.data,
            ubicacion=form.ubicacion.data,
            descripcion=form.descripcion.data,
            estado=form.estado.data,
            contract_id=form.contract_id.data
        )
        db.session.add(puesto)
        db.session.commit()

        flash("Puesto creado correctamente", "success")
        return redirect(url_for("posts.list_posts"))

    return render_template("posts/form.html", form=form, titulo="Nuevo Puesto")


@posts_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    puesto = Post.query.get_or_404(id)
    form = PostForm(obj=puesto)
    form.contract_id.choices = [
        (c.id, f"{c.id} - {c.cliente.nombre} - {c.tipo_servicio}")
        for c in Contract.query.all()
    ]

    if form.validate_on_submit():
        puesto.nombre = form.nombre.data
        puesto.ubicacion = form.ubicacion.data
        puesto.descripcion = form.descripcion.data
        puesto.estado = form.estado.data
        puesto.contract_id = form.contract_id.data

        db.session.commit()
        flash("Puesto actualizado correctamente", "success")
        return redirect(url_for("posts.list_posts"))

    return render_template("posts/form.html", form=form, titulo="Editar Puesto")


@posts_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_post(id):
    puesto = Post.query.get_or_404(id)
    db.session.delete(puesto)
    db.session.commit()

    flash("Puesto eliminado correctamente", "warning")
    return redirect(url_for("posts.list_posts"))