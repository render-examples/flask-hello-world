import os
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from models import db, Estudiantes
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

@app.route('/')
def lista_estudiantes():
    estudiantes = Estudiantes.query.all()
    return render_template('estudiantes.html', estudiantes=estudiantes)


@app.route('/Crear', methods=['GET', 'POST'])
def nuevo_estudiante():
    if request.method == 'POST':
        nombre = request.form.get('Nombre')
        apellido = request.form.get('Apellido')
        ciclo = request.form.get('Ciclo')
        programa = request.form.get('Programa')

        if nombre and apellido and ciclo and programa:
            nuevo_estudiante = Estudiantes(nombre=nombre, apellido=apellido, ciclo=ciclo, programa=programa)
            db.session.add(nuevo_estudiante)
            db.session.commit()

            return redirect(url_for('lista_estudiantes'))

    return render_template('index.html')
