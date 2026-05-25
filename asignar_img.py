# asignar_img.py
from app import create_app, db
from models import Service

app = create_app()
with app.app_context():
    imagenes = {
        1: "img/pc_mant.jpg",
        2: "img/pc_hardware.jpg",
        3: "img/software.jpg",
        4: "img/notebook_mant.jpg",
        5: "img/notebook_pantalla.jpg",
        6: "img/teclado.jpg",
        7: "img/tv_led.jpg",
        8: "img/smart_tv.jpg",
        9: "img/impresora.jpg",
        10: "img/toner.jpg",
        11: "img/audio.jpg",
        12: "img/home_theater.jpg"
    }
    
    for svc_id, ruta in imagenes.items():
        servicio = Service.query.get(svc_id)
        if servicio:
            servicio.image_url = ruta.strip()
            print(f"✅ ID {svc_id} -> {ruta}")
        else:
            print(f"⚠️ No existe servicio con ID {svc_id}")
    
    db.session.commit()
    print("\n🎉 ¡Imágenes asignadas correctamente!")