from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class VacationForm(FlaskForm):
    employee_id = SelectField("Empleado", coerce=int, validators=[DataRequired()])

    fecha_inicio = DateField("Fecha Inicio", format="%Y-%m-%d", validators=[DataRequired()])
    fecha_fin = DateField("Fecha Fin", format="%Y-%m-%d", validators=[DataRequired()])

    dias = IntegerField("Días", validators=[DataRequired(), NumberRange(min=1)])

    observacion = TextAreaField("Observación")

    estado = SelectField(
        "Estado",
        choices=[
            ("Programada", "Programada"),
            ("Aprobada", "Aprobada"),
            ("Tomada", "Tomada"),
            ("Cancelada", "Cancelada")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")