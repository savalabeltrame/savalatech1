# routes/main.py
from flask import Blueprint, render_template

# Definimos el Blueprint
main_bp = Blueprint('main', __name__)

# Ruta principal (Home)
@main_bp.route('/')
def index():
    return "<h1>✅ SavalaTech funciona correctamente!</h1><p>Tu servidor está corriendo sin errores.</p>"