from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    nombre = StringField("Nombre del Puesto", validators=[DataRequired()])
    ubicacion = StringField("Ubicación", validators=[DataRequired()])
    descripcion = StringField("Descripción")
    estado = SelectField(
        "Estado",
        choices=[
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo")
        ],
        validators=[DataRequired()]
    )
    contract_id = SelectField("Contrato", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Guardar")