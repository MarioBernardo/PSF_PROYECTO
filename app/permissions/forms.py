from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PermissionForm(FlaskForm):
    employee_id = SelectField("Empleado", coerce=int, validators=[DataRequired()])

    fecha_inicio = DateField("Fecha Inicio", format="%Y-%m-%d", validators=[DataRequired()])
    fecha_fin = DateField("Fecha Fin", format="%Y-%m-%d", validators=[DataRequired()])

    motivo = SelectField(
        "Motivo",
        choices=[
            ("Personal", "Personal"),
            ("Médico", "Médico"),
            ("Calamidad Doméstica", "Calamidad Doméstica"),
            ("Diligencia", "Diligencia"),
            ("Otro", "Otro")
        ],
        validators=[DataRequired()]
    )

    descripcion = TextAreaField("Descripción")

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Aprobado", "Aprobado"),
            ("Rechazado", "Rechazado")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar")