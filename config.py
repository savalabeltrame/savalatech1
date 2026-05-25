import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-savalatech-2026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///savalatech.db'
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # ==========================================
    # 🔍 CONFIGURACIÓN SEO (Indentación corregida)
    # ==========================================
    SEO_TITLE = "SavalaTech | Reparación Profesional de PC, Notebooks y Accesorios"
    SEO_DESCRIPTION = "Servicio técnico especializado en mantenimiento, reparación de hardware, cambio de pantallas y venta de accesorios originales. Garantía y factura PDF."
    SEO_KEYWORDS = "reparación de computadoras, técnico notebook, cambio pantalla laptop, accesorios HP Dell Apple, mantenimiento PC, SavalaTech"
    SITE_URL = "http://localhost:5001"
    DEFAULT_OG_IMAGE = "/static/img/baterias.jpg"

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
MERCADOPAGO_ACCESS_TOKEN = 'tu_token_aqui'
STRIPE_SECRET_KEY = 'sk_test_...'
STRIPE_PUBLISHABLE_KEY = 'pk_test_...'
