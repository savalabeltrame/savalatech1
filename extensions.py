# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel

# 1. Crear las instancias de las extensiones (todavía no inicializadas)
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
babel = Babel()

# 2. Configuración de LoginManager
# Esto le dice a Flask a dónde enviar al usuario si intenta entrar a una zona privada sin loguearse
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicia sesión para continuar.'
login_manager.login_message_category = 'info'