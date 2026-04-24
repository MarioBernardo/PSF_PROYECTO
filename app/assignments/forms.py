from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class AssignmentForm(FlaskForm):
    contract_id = SelectField("Contrato", coerce=int, validators=[DataRequired()])
    employee_id = SelectField("Empleado", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Asignar")