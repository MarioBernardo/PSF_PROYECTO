import os
from werkzeug.utils import secure_filename

from flask import render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required

from app.documents import documents_bp
from app.documents.forms import DocumentForm
from app.extensions import db
from app.models import Document, Employee, Client


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "documentos")


@documents_bp.route("/")
@login_required
def list_documents():
    documentos = Document.query.order_by(Document.id.desc()).all()
    return render_template("documents/list.html", documentos=documentos)


def cargar_listas(form):
    form.employee_id.choices = [(0, "Ninguno")] + [
        (e.id, f"{e.apellidos} {e.nombres}")
        for e in Employee.query.all()
    ]

    form.client_id.choices = [(0, "Ninguno")] + [
        (c.id, c.nombre)
        for c in Client.query.all()
    ]


@documents_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_document():
    form = DocumentForm()
    cargar_listas(form)

    if form.validate_on_submit():

        if not form.archivo.data:
            flash("Debe seleccionar archivo", "danger")
            return redirect(url_for("documents.create_document"))

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        archivo = form.archivo.data
        nombre = secure_filename(archivo.filename)

        ruta = os.path.join(UPLOAD_FOLDER, nombre)
        archivo.save(ruta)

        nuevo = Document(
            numero=form.numero.data,
            tipo=form.tipo.data,
            estado=form.estado.data,
            titulo=form.titulo.data,
            employee_id=form.employee_id.data if form.employee_id.data != 0 else None,
            client_id=form.client_id.data if form.client_id.data != 0 else None,
            fecha=form.fecha.data,
            archivo=nombre,
            observacion=form.observacion.data
        )

        db.session.add(nuevo)
        db.session.commit()

        flash("Documento guardado correctamente", "success")
        return redirect(url_for("documents.list_documents"))

    return render_template("documents/form.html", form=form, titulo="Nuevo Documento")


@documents_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_document(id):
    doc = Document.query.get_or_404(id)

    form = DocumentForm(obj=doc)
    cargar_listas(form)

    if form.validate_on_submit():

        doc.numero = form.numero.data
        doc.tipo = form.tipo.data
        doc.estado = form.estado.data
        doc.titulo = form.titulo.data
        doc.employee_id = form.employee_id.data if form.employee_id.data != 0 else None
        doc.client_id = form.client_id.data if form.client_id.data != 0 else None
        doc.fecha = form.fecha.data
        doc.observacion = form.observacion.data

        if form.archivo.data:
            archivo = form.archivo.data
            nombre = secure_filename(archivo.filename)

            ruta = os.path.join(UPLOAD_FOLDER, nombre)
            archivo.save(ruta)

            doc.archivo = nombre

        db.session.commit()

        flash("Documento actualizado correctamente", "success")
        return redirect(url_for("documents.list_documents"))

    return render_template("documents/form.html", form=form, titulo="Editar Documento")


@documents_bp.route("/download/<path:filename>")
@login_required
def download_document(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True
    )


@documents_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_document(id):
    doc = Document.query.get_or_404(id)

    ruta = os.path.join(UPLOAD_FOLDER, doc.archivo)

    if os.path.exists(ruta):
        os.remove(ruta)

    db.session.delete(doc)
    db.session.commit()

    flash("Documento eliminado", "warning")
    return redirect(url_for("documents.list_documents"))