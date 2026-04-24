from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SelectField, StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class DocumentForm(FlaskForm):
    numero = StringField("Número Documento")

    tipo = SelectField(
        "Tipo Documento",
        choices=[
            ("Factura SRI", "Factura SRI"),
            ("Recibo", "Recibo"),
            ("Contrato Cliente", "Contrato Cliente"),
            ("Contrato Empleado", "Contrato Empleado"),
            ("Memorando", "Memorando"),
            ("Cotización", "Cotización"),
            ("Acta Entrega", "Acta Entrega"),
            ("Reglamento", "Reglamento"),
            ("Otro", "Otro"),
        ],
        validators=[DataRequired()]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Enviado", "Enviado"),
            ("Firmado", "Firmado"),
            ("Pagado", "Pagado"),
            ("Archivado", "Archivado"),
        ],
        validators=[DataRequired()]
    )

    titulo = StringField("Título", validators=[DataRequired()])
    employee_id = SelectField("Empleado", coerce=int, choices=[])
    client_id = SelectField("Cliente", coerce=int, choices=[])
    fecha = DateField("Fecha", format="%Y-%m-%d", validators=[DataRequired()])
    archivo = FileField("Archivo")
    observacion = TextAreaField("Observación")

    submit = SubmitField("Guardar")