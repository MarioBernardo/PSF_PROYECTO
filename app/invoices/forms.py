from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional


class InvoiceForm(FlaskForm):
    client_id = SelectField("Cliente", coerce=int, choices=[], validators=[DataRequired()])

    numero = StringField("Número Comprobante", validators=[DataRequired()])

    tipo_comprobante = SelectField(
        "Tipo Comprobante",
        choices=[
            ("Factura", "Factura"),
            ("Recibo", "Recibo"),
        ],
        validators=[DataRequired()]
    )

    mes = StringField("Mes Facturado", validators=[DataRequired()])
    fecha = DateField("Fecha Emisión", format="%Y-%m-%d", validators=[DataRequired()])
    fecha_vencimiento = DateField("Fecha Vencimiento", format="%Y-%m-%d", validators=[Optional()])

    subtotal = FloatField("Subtotal", validators=[DataRequired()])

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Enviada", "Enviada"),
            ("Pagada", "Pagada"),
            ("Vencida", "Vencida"),
            ("Anulada", "Anulada"),
        ],
        validators=[DataRequired()]
    )

    observacion = TextAreaField("Observación")
    submit = SubmitField("Guardar")