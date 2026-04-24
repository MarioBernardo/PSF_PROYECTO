from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired


class InventoryForm(FlaskForm):
    nombre = StringField("Nombre del Equipo", validators=[DataRequired()])

    categoria = SelectField(
        "Categoría",
        choices=[
            ("Radio", "Radio"),
            ("Linterna", "Linterna"),
            ("Chaleco", "Chaleco"),
            ("Uniforme", "Uniforme"),
            ("Computador", "Computador"),
            ("Accesorio", "Accesorio"),
            ("Otro", "Otro")
        ],
        validators=[DataRequired()]
    )

    codigo = StringField("Código", validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired()])

    estado = SelectField(
        "Estado",
        choices=[
            ("Disponible", "Disponible"),
            ("Asignado", "Asignado"),
            ("Dañado", "Dañado"),
            ("Mantenimiento", "Mantenimiento"),
            ("Baja", "Baja")
        ],
        validators=[DataRequired()]
    )

    observacion = StringField("Observación")

    post_id = SelectField("Puesto", coerce=int, validators=[DataRequired()])

    submit = SubmitField("Guardar")