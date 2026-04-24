from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class DelayForm(FlaskForm):
    employee_id = SelectField("Empleado", coerce=int, validators=[DataRequired()])
    shift_id = SelectField("Turno", coerce=int, validators=[DataRequired()])

    fecha = DateField("Fecha", format="%Y-%m-%d", validators=[DataRequired()])
    minutos = IntegerField("Minutos de atraso", validators=[DataRequired(), NumberRange(min=1)])

    motivo = StringField("Motivo")

    estado = SelectField(
        "Estado",
        choices=[
            ("Registrado", "Registrado"),
            ("Justificado", "Justificado"),
            ("Injustificado", "Injustificado")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")