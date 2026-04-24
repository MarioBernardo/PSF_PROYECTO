from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()

    usuarios = [
        ("admin", "admin@test.com", "1234", "admin"),
        ("supervisor1", "supervisor@test.com", "1234", "supervisor"),
        ("rrhh1", "rrhh@test.com", "1234", "rrhh"),
        ("operador1", "operador@test.com", "1234", "operador"),
    ]

    for username, email, password, role in usuarios:
        existe = User.query.filter_by(username=username).first()
        if not existe:
            user = User(username=username, email=email, role=role)
            user.set_password(password)
            db.session.add(user)

    db.session.commit()
    print("Usuarios verificados/creados")