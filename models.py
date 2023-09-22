from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Estudiantes(db.Model):
    __tablename__ = "Estudiantes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    ciclo = db.Column(db.String, nullable=False)
    programa = db.Column(db.String, nullable=False)