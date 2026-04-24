from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired


class PayrollForm(FlaskForm):
    employee_id = SelectField(
        "Empleado",
        coerce=int,
        validators=[DataRequired()]
    )

    mes = SelectField(
        "Mes",
        choices=[
            ("ENERO", "ENERO"),
            ("FEBRERO", "FEBRERO"),
            ("MARZO", "MARZO"),
            ("ABRIL", "ABRIL"),
            ("MAYO", "MAYO"),
            ("JUNIO", "JUNIO"),
            ("JULIO", "JULIO"),
            ("AGOSTO", "AGOSTO"),
            ("SEPTIEMBRE", "SEPTIEMBRE"),
            ("OCTUBRE", "OCTUBRE"),
            ("NOVIEMBRE", "NOVIEMBRE"),
            ("DICIEMBRE", "DICIEMBRE"),
        ],
        validators=[DataRequired()]
    )

    anio = IntegerField(
        "Año",
        validators=[DataRequired()]
    )

    tipo_pago = SelectField(
        "Tipo de Pago",
        choices=[
            ("mensual", "Mensual"),
            ("turno", "Por Turno / Sacafrancos"),
        ],
        validators=[DataRequired()]
    )

    base_iess = SelectField(
        "Base Cálculo IESS",
        choices=[
            ("basico", "Solo Sueldo Básico"),
            ("total", "Sueldo + Horas Extras"),
        ],
        validators=[DataRequired()]
    )

    turnos_realizados = IntegerField(
        "Turnos Realizados",
        default=0
    )

    valor_turno = FloatField(
        "Valor por Turno",
        default=0
    )

    sueldo_basico = FloatField(
        "Sueldo Básico",
        default=0
    )

    horas_extras = FloatField(
        "Horas Extras",
        default=0
    )

    otros_ingresos = FloatField(
        "Otros Ingresos",
        default=0
    )

    prestamo_quirografario = FloatField(
        "Préstamos Quirografarios IESS",
        default=0
    )

    anticipo_empresa = FloatField(
        "Anticipo Empresa",
        default=0
    )

    multas = FloatField(
        "Multas",
        default=0
    )

    otros_descuentos = FloatField(
        "Otros Descuentos",
        default=0
    )

    submit = SubmitField("Guardar Rol")