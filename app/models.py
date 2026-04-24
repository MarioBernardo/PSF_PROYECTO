from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="operador")
    is_active_user = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=True)
    tipo_puesto = db.Column(db.String(30))
    cargo = db.Column(db.String(50))
    salario = db.Column(db.Float)

class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    ruc_ci = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(120))

class Contract(db.Model):
    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    tipo_servicio = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(50), default="Activo")

    cliente = db.relationship("Client", backref="contratos")

class ContractEmployee(db.Model):
    __tablename__ = "contract_employees"

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)

    contract = db.relationship("Contract", backref="asignaciones")
    employee = db.relationship("Employee", backref="asignaciones")

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(200))
    estado = db.Column(db.String(30), default="Activo")

    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id"), nullable=False)
    contract = db.relationship("Contract", backref="puestos")

class Shift(db.Model):
    __tablename__ = "shifts"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    fecha = db.Column(db.Date, nullable=False)
    tipo_turno = db.Column(db.String(20), nullable=False)  # 12 horas / 24 horas
    estado = db.Column(db.String(30), default="Programado")

    employee = db.relationship("Employee", backref="turnos")
    post = db.relationship("Post", backref="turnos")

class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"), nullable=False)

    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(30), default="Pendiente")

    employee = db.relationship("Employee", backref="novedades")
    shift = db.relationship("Shift", backref="novedades")

class Inventory(db.Model):
    __tablename__ = "inventories"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    estado = db.Column(db.String(30), default="Disponible")
    observacion = db.Column(db.String(200))

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    post = db.relationship("Post", backref="inventarios")

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.String(30), default="Pendiente")

    employee = db.relationship("Employee", backref="permisos")

class Vacation(db.Model):
    __tablename__ = "vacations"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    observacion = db.Column(db.Text)
    estado = db.Column(db.String(30), default="Programada")

    employee = db.relationship("Employee", backref="vacaciones")

class Delay(db.Model):
    __tablename__ = "delays"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey("shifts.id"), nullable=False)

    fecha = db.Column(db.Date, nullable=False)
    minutos = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(150))
    estado = db.Column(db.String(30), default="Registrado")

    employee = db.relationship("Employee", backref="atrasos")
    shift = db.relationship("Shift", backref="atrasos")

class Payroll(db.Model):
    __tablename__ = "payrolls"

    id = db.Column(db.Integer, primary_key=True)
    numero_rol = db.Column(db.String(30), unique=True, nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    mes = db.Column(db.String(20), nullable=False)
    anio = db.Column(db.Integer, nullable=False)

    tipo_pago = db.Column(db.String(30), default="mensual")
    base_iess = db.Column(db.String(30), default="basico")
    turnos_realizados = db.Column(db.Integer, default=0)
    valor_turno = db.Column(db.Float, default=0)

    sueldo_basico = db.Column(db.Float, default=0)
    horas_extras = db.Column(db.Float, default=0)
    decimo_tercero = db.Column(db.Float, default=0)
    decimo_cuarto = db.Column(db.Float, default=0)
    fondos_reserva = db.Column(db.Float, default=0)
    otros_ingresos = db.Column(db.Float, default=0)

    aporte_iess = db.Column(db.Float, default=0)
    prestamo_quirografario = db.Column(db.Float, default=0)
    anticipo_empresa = db.Column(db.Float, default=0)
    multas = db.Column(db.Float, default=0)
    otros_descuentos = db.Column(db.Float, default=0)

    total_ingresos = db.Column(db.Float, default=0)
    total_descuentos = db.Column(db.Float, default=0)
    neto_pagar = db.Column(db.Float, default=0)

    employee = db.relationship("Employee", backref="roles_pago")

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)

    numero = db.Column(db.String(50))
    tipo = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(30), default="Pendiente")

    titulo = db.Column(db.String(200), nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))

    fecha = db.Column(db.Date, nullable=False)

    archivo = db.Column(db.String(255), nullable=False)

    observacion = db.Column(db.Text)

    employee = db.relationship("Employee", backref="documentos")
    client = db.relationship("Client", backref="documentos")

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))

    numero = db.Column(db.String(50), nullable=False)
    tipo_comprobante = db.Column(db.String(20), default="Factura")
    mes = db.Column(db.String(30), nullable=False)

    fecha = db.Column(db.Date, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=True)

    subtotal = db.Column(db.Float, default=0)
    iva = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    estado = db.Column(db.String(20), default="Pendiente")
    observacion = db.Column(db.Text)

    client = db.relationship("Client", backref="facturas")

class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id")
    )

    fecha = db.Column(db.Date, nullable=False)

    estado = db.Column(
        db.String(20),
        nullable=False
    )

    observacion = db.Column(db.Text)

    employee = db.relationship(
        "Employee",
        backref="asistencias"
    )