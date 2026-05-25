from app import create_app, db
from models import Service

app = create_app()
with app.app_context():
    servicios_imagenes = {
        "Mantenimiento Preventivo PC": "img/pc_mantenimiento.jpg",
        "Reparación de Hardware PC": "img/pc_hardware.jpg",
        "Instalación de Software": "img/software.jpg",
        "Mantenimiento Notebook": "img/notebook_mantenimiento.jpg",
        "Cambio de Pantalla Notebook": "img/notebook_pantalla.jpg",
        "Reparación de Teclado": "img/teclado.jpg",
        "Reparación de TV LED/LCD": "img/tv_reparacion.jpg",
        "Configuración Smart TV": "img/smart_tv.jpg",
        "Mantenimiento de Impresora": "img/impresora.jpg",
        "Recarga de Tóner": "img/toner.jpg",
        "Reparación de Equipos de Sonido": "img/audio.jpg",
        "Configuración Home Theater": "img/home_theater.jpg"
    }
    
    actualizados = 0
    for nombre, ruta in servicios_imagenes.items():
        servicio = Service.query.filter_by(name_es=nombre.strip()).first()
        if servicio:
            servicio.image_url = ruta.strip()
            actualizados += 1
            print(f"✅ {nombre} -> {ruta}")
        else:
            print(f"⚠️ No encontrado: {nombre}")
    
    db.session.commit()
    print(f"\n🎉 {actualizados} servicios actualizados")