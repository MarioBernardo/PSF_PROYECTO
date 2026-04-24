from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    DateField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import DataRequired


class AttendanceForm(FlaskForm):

    employee_id = SelectField(
        "Empleado",
        coerce=int,
        choices=[],
        validators=[DataRequired()]
    )

    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Presente", "Presente"),
            ("Libre", "Libre"),
            ("Falta", "Falta"),
            ("Permiso", "Permiso"),
            ("Atrasado", "Atrasado"),
            ("Vacaciones", "Vacaciones  "),
        ],
        validators=[DataRequired()]
    )

    observacion = TextAreaField("Observación")

    submit = SubmitField("Guardar")