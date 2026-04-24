from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class IncidentForm(FlaskForm):
    employee_id = SelectField("Empleado", coerce=int, validators=[DataRequired()])
    shift_id = SelectField("Turno", coerce=int, validators=[DataRequired()])

    tipo = SelectField(
        "Tipo de Novedad",
        choices=[
            ("Atraso", "Atraso"),
            ("Falta", "Falta"),
            ("Incidente", "Incidente"),
            ("Observación", "Observación"),
            ("Permiso", "Permiso"),
            ("Otro", "Otro")
        ],
        validators=[DataRequired()]
    )

    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    fecha = DateField("Fecha", format="%Y-%m-%d", validators=[DataRequired()])

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Revisado", "Revisado"),
            ("Cerrado", "Cerrado")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")