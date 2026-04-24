from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional


class ClientForm(FlaskForm):
    nombre = StringField("Nombre del Cliente", validators=[DataRequired()])
    ruc_ci = StringField("RUC / Cédula")
    direccion = StringField("Dirección")
    telefono = StringField("Teléfono")
    correo = StringField("Correo", validators=[Optional(), Email()])
    submit = SubmitField("Guardar")