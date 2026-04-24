from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class UserForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField("Correo", validators=[DataRequired(), Email()])

    role = SelectField(
        "Rol",
        choices=[
            ("admin", "Administrador"),
            ("supervisor", "Supervisor"),
            ("rrhh", "RRHH"),
            ("operador", "Operador")
        ],
        validators=[DataRequired()]
    )

    password = PasswordField("Contraseña", validators=[Optional(), Length(min=4)])
    confirm_password = PasswordField(
        "Confirmar Contraseña",
        validators=[Optional(), EqualTo("password", message="Las contraseñas no coinciden")]
    )

    submit = SubmitField("Guardar")