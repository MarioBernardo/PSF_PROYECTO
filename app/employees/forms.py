from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired


class EmployeeForm(FlaskForm):
    nombres = StringField("Nombres", validators=[DataRequired()])
    apellidos = StringField("Apellidos", validators=[DataRequired()])
    cedula = StringField("Cédula", validators=[DataRequired()])
    fecha_ingreso = DateField("Fecha de Ingreso", format="%Y-%m-%d", validators=[DataRequired()])

    tipo_puesto = SelectField(
        "Tipo de Puesto",
        choices=[
            ("Fijo", "Fijo"),
            ("Ocasional", "Ocasional")
        ],
        validators=[DataRequired()]
    )

    cargo = SelectField(
        "Cargo",
        choices=[
            ("Guardia", "Guardia"),
            ("Supervisor", "Supervisor"),
            ("Sacafrancos", "Sacafrancos"),
            ("Administrativo", "Administrativo"),
            ("Coordinador", "Coordinador"),
            ("Jefe de Operaciones", "Jefe de Operaciones"),
            ("Monitorista", "Monitorista"),
            ("Recepcionista", "Recepcionista")
        ],
        validators=[DataRequired()]
    )

    salario = FloatField("Salario")
    submit = SubmitField("Guardar")