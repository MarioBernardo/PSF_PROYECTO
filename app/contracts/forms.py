from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import DataRequired


class ContractForm(FlaskForm):
    cliente_id = SelectField("Cliente", coerce=int, validators=[DataRequired()])

    tipo_servicio = SelectField(
        "Tipo de Servicio",
        choices=[
            ("Vigilancia Fija", "Vigilancia Fija"),
            ("Custodia", "Custodia"),
            ("Seguridad Electrónica", "Seguridad Electrónica"),
            ("Monitoreo", "Monitoreo"),
            ("Control de Accesos", "Control de Accesos")
        ],
        validators=[DataRequired()]
    )

    fecha_inicio = DateField("Fecha Inicio", format="%Y-%m-%d", validators=[DataRequired()])
    fecha_fin = DateField("Fecha Fin", format="%Y-%m-%d", validators=[DataRequired()])

    estado = SelectField(
        "Estado",
        choices=[
            ("Activo", "Activo"),
            ("Suspendido", "Suspendido"),
            ("Finalizado", "Finalizado")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")