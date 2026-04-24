from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired


class ShiftForm(FlaskForm):
    employee_id = SelectField("Empleado", coerce=int, validators=[DataRequired()])
    post_id = SelectField("Puesto", coerce=int, validators=[DataRequired()])

    fecha = DateField("Fecha", format="%Y-%m-%d", validators=[DataRequired()])

    tipo_turno = SelectField(
        "Tipo de Turno",
        choices=[
            ("12 horas", "12 horas"),
            ("24 horas", "24 horas")
        ],
        validators=[DataRequired()]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Programado", "Programado"),
            ("Cumplido", "Cumplido"),
            ("Pendiente", "Pendiente"),
            ("Cancelado", "Cancelado")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")