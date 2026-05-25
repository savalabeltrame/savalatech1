import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ← Tus imports originales van DESPUÉS de estas líneas
from extensions import db, login_manager, mail, babel

import os
import io
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, render_template, flash, send_file, current_app
from config import config
from extensions import db, login_manager, mail, babel
from models import User, Service, Order, OrderItem, Invoice, CartItem
from fpdf import FPDF
import mercadopago

# ==========================================
# DATOS GLOBALES
# ==========================================

TRANSLATIONS = {
    'es': {
        'inicio': 'Inicio', 'accesorios': 'Accesorios', 'blog': 'Blog', 'testimonios': 'Testimonios', 'carrito': 'Carrito', 'equipo': 'Equipo',
        'titulo_hero': 'Clínica de Computadoras', 'subtitulo_hero': 'Asistencia Técnica Especializada',
        'desc_hero': 'Somos una empresa especializada en la reparación y mantenimiento de equipos informáticos.',
        'btn_servicios': 'Ver Servicios', 'btn_video': 'Ver Video', 'titulo_repuestos': 'Tienda de Repuestos',
        'footer_about': 'Reparación profesional de equipos informáticos con garantía.',
        'footer_contact': 'Contacto', 'footer_follow': 'Síguenos', 'footer_rights': '© 2026 SavalaTech. Todos los derechos reservados.',
        'blog_title': 'Blog Técnico', 'read_more': 'Leer más',
        'team_title': 'Nuestro Equipo', 'team_subtitle': 'Expertos en Reparación',
        'spec_pc': 'Especialista PC', 'spec_notebook': 'Experto Notebooks', 'spec_macbook': 'Técnico Apple/MacBook', 'spec_hardware': 'Especialista Hardware',
        'video_title': 'Reparación de Laptop - Paso a Paso', 'video_desc': 'Mira cómo reparamos una notebook desde cero',
        'search_placeholder': 'Buscar por modelo (ej: HP Pavilion, iPhone 11...)', 'btn_search': 'Buscar', 'btn_all': 'Todos',
        'lbl_brand': 'Marca', 'lbl_all_brands': 'Todas las marcas', 'lbl_stock': 'Stock', 'btn_details': 'Ver Detalles',
        'no_products': 'No se encontraron productos', 'clear_search': 'Limpiar búsqueda',
        'payment_title': 'Método de Pago', 'payment_cash': 'Efectivo', 'payment_pix': 'Pix', 'payment_card': 'Tarjeta de Crédito',
        'checkout_btn': 'Confirmar Compra', 'success_title': '¡Compra Exitosa!', 'success_desc': 'Tu orden ha sido procesada correctamente.',
        'download_pdf': 'Descargar Factura PDF', 'order_id': 'N° de Orden', 'payment_method': 'Método de Pago', 'total_paid': 'Total Pagado',
        'services_label': '🛠️ Servicios de Reparación', 'accessories_label': '📦 Accesorios y Repuestos'
    },
    'pt_BR': {
        'inicio': 'Início', 'accesorios': 'Acessórios', 'blog': 'Blog', 'testimonios': 'Depoimentos', 'carrito': 'Carrinho', 'equipo': 'Equipe',
        'titulo_hero': 'Clínica De Computadores', 'subtitulo_hero': 'Assistência Técnica Especializada',
        'desc_hero': 'Somos uma empresa especializada na reparação e manutenção de equipamentos informáticos.',
        'btn_servicios': 'Ver Serviços', 'btn_video': 'Ver Vídeo', 'titulo_repuestos': 'Loja de Peças',
        'footer_about': 'Reparação profissional de equipamentos informáticos com garantia.',
        'footer_contact': 'Contato', 'footer_follow': 'Siga-nos', 'footer_rights': '© 2026 SavalaTech. Todos os direitos reservados.',
        'blog_title': 'Blog Técnico', 'read_more': 'Ler mais',
        'team_title': 'Nossa Equipe', 'team_subtitle': 'Especialistas em Reparo',
        'spec_pc': 'Especialista PC', 'spec_notebook': 'Expert Notebooks', 'spec_macbook': 'Técnico Apple/MacBook', 'spec_hardware': 'Especialista Hardware',
        'video_title': 'Reparação de Laptop - Passo a Passo', 'video_desc': 'Veja como consertamos um notebook do zero',
        'search_placeholder': 'Buscar por modelo (ex: HP Pavilion, iPhone 11...)', 'btn_search': 'Buscar', 'btn_all': 'Todos',
        'lbl_brand': 'Marca', 'lbl_all_brands': 'Todas as marcas', 'lbl_stock': 'Estoque', 'btn_details': 'Ver Detalhes',
        'no_products': 'Nenhum produto encontrado', 'clear_search': 'Limpar busca',
        'payment_title': 'Método de Pagamento', 'payment_cash': 'Dinheiro', 'payment_pix': 'Pix', 'payment_card': 'Cartão de Crédito',
        'checkout_btn': 'Confirmar Compra', 'success_title': 'Compra Realizada!', 'success_desc': 'Seu pedido foi processado corretamente.',
        'download_pdf': 'Baixar Fatura PDF', 'order_id': 'N° do Pedido', 'payment_method': 'Método de Pagamento', 'total_paid': 'Total Pago',
        'services_label': '🛠️ Serviços de Reparo', 'accessories_label': '📦 Acessórios e Peças'
    },
    'en': {
        'inicio': 'Home', 'accesorios': 'Accessories', 'blog': 'Blog', 'testimonios': 'Testimonials', 'carrito': 'Cart', 'equipo': 'Team',
        'titulo_hero': 'Computer Clinic', 'subtitulo_hero': 'Specialized Technical Assistance',
        'desc_hero': 'We are a company specialized in the repair and maintenance of IT equipment.',
        'btn_servicios': 'View Services', 'btn_video': 'Watch Video', 'titulo_repuestos': 'Parts Store',
        'footer_about': 'Professional IT equipment repair with warranty.',
        'footer_contact': 'Contact', 'footer_follow': 'Follow Us', 'footer_rights': '© 2026 SavalaTech. All rights reserved.',
        'blog_title': 'Technical Blog', 'read_more': 'Read more',
        'team_title': 'Our Team', 'team_subtitle': 'Repair Experts',
        'spec_pc': 'PC Specialist', 'spec_notebook': 'Notebook Expert', 'spec_macbook': 'Apple/MacBook Tech', 'spec_hardware': 'Hardware Specialist',
        'video_title': 'Laptop Repair - Step by Step', 'video_desc': 'See how we repair a notebook from scratch',
        'search_placeholder': 'Search by model (e.g.: HP Pavilion, iPhone 11...)', 'btn_search': 'Search', 'btn_all': 'All',
        'lbl_brand': 'Brand', 'lbl_all_brands': 'All brands', 'lbl_stock': 'Stock', 'btn_details': 'View Details',
        'no_products': 'No products found', 'clear_search': 'Clear search',
        'payment_title': 'Payment Method', 'payment_cash': 'Cash', 'payment_pix': 'Pix', 'payment_card': 'Credit Card',
        'checkout_btn': 'Confirm Purchase', 'success_title': 'Purchase Successful!', 'success_desc': 'Your order has been processed correctly.',
        'download_pdf': 'Download Invoice PDF', 'order_id': 'Order #', 'payment_method': 'Payment Method', 'total_paid': 'Total Paid',
        'services_label': '🛠️ Repair Services', 'accessories_label': '📦 Accessories & Parts'
    }
}

CATEGORIES = [
    {'id': 'baterias-notebook', 'name_es': 'Baterías Notebook', 'name_pt': 'Baterias Notebook', 'name_en': 'Notebook Batteries', 'icon': 'fa-battery-full'},
    {'id': 'baterias-celular', 'name_es': 'Baterías Celular', 'name_pt': 'Baterias Celular', 'name_en': 'Phone Batteries', 'icon': 'fa-mobile-screen'},
    {'id': 'displays-notebook', 'name_es': 'Displays Notebook', 'name_pt': 'Telas Notebook', 'name_en': 'Notebook Displays', 'icon': 'fa-laptop'},
    {'id': 'teclados', 'name_es': 'Teclados', 'name_pt': 'Teclados', 'name_en': 'Keyboards', 'icon': 'fa-keyboard'},
    {'id': 'cargadores', 'name_es': 'Cargadores', 'name_pt': 'Carregadores', 'name_en': 'Chargers', 'icon': 'fa-plug'},
]

ACCESSORIES_DB = {
    'baterias-notebook': [
        {'id': 1, 'name': 'Batería HP Pavilion 15', 'brand': 'HP', 'model': 'Pavilion 15', 'price': 230.00, 'stock': 10, 'image': '/static/img/bateria-hp.jpg'},
        {'id': 2, 'name': 'Batería Dell Inspiron 15', 'brand': 'Dell', 'model': 'Inspiron 15', 'price': 192.00, 'stock': 8, 'image': '/static/img/bateria-dell.jpg'},
        {'id': 3, 'name': 'Batería Lenovo IdeaPad', 'brand': 'Lenovo', 'model': 'IdeaPad 3', 'price': 220.00, 'stock': 12, 'image': '/static/img/bateria-hp.jpg'},
    ],
    'baterias-celular': [
        {'id': 6, 'name': 'Batería iPhone 11', 'brand': 'Apple', 'model': 'iPhone 11', 'price': 180.00, 'stock': 20, 'image': '/static/img/bateria-iphone.jpg'},
        {'id': 7, 'name': 'Batería Samsung S20', 'brand': 'Samsung', 'model': 'Galaxy S20', 'price': 199.00, 'stock': 25, 'image': '/static/img/bateria-samsung.jpg'},
        {'id': 8, 'name': 'Batería Xiaomi Redmi', 'brand': 'Xiaomi', 'model': 'Redmi Note 9', 'price': 155.00, 'stock': 30, 'image': '/static/img/bateria-xiaomi.jpg'},
    ],
    'displays-notebook': [
        {'id': 11, 'name': 'Pantalla HP 15.6" HD', 'brand': 'HP', 'model': '15.6 HD', 'price': 450.00, 'stock': 6, 'image': '/static/img/pantalla.jpg'},
        {'id': 12, 'name': 'Pantalla Dell 15.6" FHD', 'brand': 'Dell', 'model': '15.6 FHD IPS', 'price': 520.00, 'stock': 4, 'image': '/static/img/pantalla.jpg'},
        {'id': 13, 'name': 'Pantalla MacBook 13"', 'brand': 'Apple', 'model': 'MacBook Pro 13', 'price': 2450.00, 'stock': 3, 'image': '/static/img/pantalla.jpg'},
    ],
    'teclados': [
        {'id': 15, 'name': 'Teclado HP US', 'brand': 'HP', 'model': 'Pavilion US', 'price': 180.00, 'stock': 15, 'image': '/static/img/teclado.jpg'},
        {'id': 16, 'name': 'Teclado Dell ES', 'brand': 'Dell', 'model': 'Inspiron ES', 'price': 195.00, 'stock': 12, 'image': '/static/img/teclado1.jpg'},
        {'id': 17, 'name': 'Teclado Lenovo', 'brand': 'Lenovo', 'model': 'IdeaPad', 'price': 185.00, 'stock': 10, 'image': '/static/img/teclado1.jpg'},
    ],
    'cargadores': [
        {'id': 18, 'name': 'Cargador HP 65W', 'brand': 'HP', 'model': '65W Blue Tip', 'price': 145.00, 'stock': 20, 'image': '/static/img/cargador-hp65.jpg'},
        {'id': 19, 'name': 'Cargador Dell 90W', 'brand': 'Dell', 'model': '90W Large Tip', 'price': 175.00, 'stock': 18, 'image': '/static/img/cargadores2.jpg'},
        {'id': 20, 'name': 'Cargador Lenovo 65W', 'brand': 'Lenovo', 'model': '65W Square', 'price': 160.00, 'stock': 22, 'image': '/static/img/cargador5.jpg'},
        {'id': 21, 'name': 'Cargador MacBook 61W', 'brand': 'Apple', 'model': 'USB-C 61W', 'price': 380.00, 'stock': 8, 'image': '/static/img/cargador2.jpg'},
    ]
}

BLOG_POSTS = {
    1: {
        'id': 1,
        'title_es': 'Cómo limpiar tu PC correctamente', 'title_pt': 'Como limpar seu PC corretamente', 'title_en': 'How to clean your PC properly',
        'date': '20 Mayo, 2026', 'author': 'Equipo SavalaTech',
        'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800',
        'excerpt_es': 'Aprende a eliminar el polvo sin dañar los componentes.', 'excerpt_pt': 'Aprenda a remover a poeira.', 'excerpt_en': 'Learn to remove dust.',
        'content_es': '<p>Usa aire comprimido, paños de microfibra y alcohol isopropílico. Limpia cada 3-6 meses.</p>', 'content_pt': '<p>Use ar comprimido e álcool.</p>', 'content_en': '<p>Use compressed air.</p>'
    },
    2: {
        'id': 2,
        'title_es': '5 Tips para tu batería', 'title_pt': '5 Dicas para sua bateria', 'title_en': '5 Tips for your battery',
        'date': '18 Mayo, 2026', 'author': 'Equipo SavalaTech',
        'image': 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800',
        'excerpt_es': 'Hábitos para mayor duración.', 'excerpt_pt': 'Hábitos para maior duração.', 'excerpt_en': 'Habits for longer life.',
        'content_es': '<p>No descargues completamente y evita el calor extremo.</p>', 'content_pt': '<p>Não descarregue completamente.</p>', 'content_en': '<p>Do not discharge completely.</p>'
    },
    3: {
        'id': 3,
        'title_es': 'HDD vs SSD: ¿Vale la pena?', 'title_pt': 'HDD vs SSD: Vale a pena?', 'title_en': 'HDD vs SSD: Is it worth it?',
        'date': '15 Mayo, 2026', 'author': 'Equipo SavalaTech',
        'image': 'https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=800',
        'excerpt_es': 'Un SSD hace tu equipo 10 veces más rápido.', 'excerpt_pt': 'Um SSD torna seu equipamento 10x mais rápido.', 'excerpt_en': 'An SSD makes your equipment 10x faster.',
        'content_es': '<p>El SSD es más rápido y resistente. Si tu PC tarda en encender, cámbialo.</p>', 'content_pt': '<p>O SSD é mais rápido e resistente.</p>', 'content_en': '<p>The SSD is faster and resistant.</p>'
    }
}

# ==========================================
# CREACIÓN DE LA APP
# ==========================================

def get_locale():
    return session.get('language', 'es')

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_translations():
        lang = session.get('language', 'es')
        return {'lang': lang, 't': TRANSLATIONS.get(lang, TRANSLATIONS['es'])}

    @app.context_processor
    def inject_config():
        return {'config': current_app.config}

    # === IDIOMAS ===
    @app.route('/set_language/<lang>')
    def set_language(lang):
        if lang in ['es', 'pt_BR', 'en']:
            session['language'] = lang
        return redirect(request.referrer or url_for('index'))

    # === RUTAS PRINCIPALES ===
    @app.route('/')
    def index():
        services = Service.query.all()
        return render_template('index.html', services=services, cart_count=get_cart_count())

    @app.route('/team')
    def team():
        return render_template('team.html', cart_count=get_cart_count())
    
    @app.route('/testimonials')
    def testimonials():
        return render_template('testimonials.html', cart_count=get_cart_count())

    @app.route('/accessories')
    def accessories():
        lang = session.get('language', 'es')
        category_id = request.args.get('category', 'all')
        search = request.args.get('search', '')
        brand = request.args.get('brand', 'all')
        
        all_brands = set()
        for cat_items in ACCESSORIES_DB.values():
            for item in cat_items:
                all_brands.add(item['brand'])
        
        products = []
        if category_id == 'all':
            for cat_items in ACCESSORIES_DB.values():
                products.extend(cat_items)
        else:
            products = ACCESSORIES_DB.get(category_id, [])
        
        if search:
            s = search.lower()
            products = [p for p in products if s in p['name'].lower() or s in p['model'].lower()]
        if brand != 'all':
            products = [p for p in products if p['brand'] == brand]
            
        return render_template('accessories.html', products=products, categories=CATEGORIES,
                               brands=sorted(list(all_brands)), current_category=category_id,
                               current_brand=brand, search_query=search, cart_count=get_cart_count())

    @app.route('/accessory/<int:accessory_id>')
    def accessory_detail(accessory_id):
        for cat_items in ACCESSORIES_DB.values():
            for item in cat_items:
                if item['id'] == accessory_id:
                    return render_template('accessory_detail.html', accessory=item, cart_count=get_cart_count())
        flash('Producto no encontrado', 'warning')
        return redirect(url_for('accessories'))

    @app.route('/blog')
    def blog():
        lang = session.get('language', 'es')
        posts = [{'id': p['id'], 'title': p.get(f'title_{lang}', p['title_es']), 'date': p['date'], 
                  'author': p['author'], 'image': p['image'], 'excerpt': p.get(f'excerpt_{lang}', p['excerpt_es'])} 
                 for p in BLOG_POSTS.values()]
        return render_template('blog.html', posts=posts, cart_count=get_cart_count())

    @app.route('/blog/<int:post_id>')
    def blog_detail(post_id):
        lang = session.get('language', 'es')
        p = BLOG_POSTS.get(post_id)
        if not p:
            return "No encontrado", 404
        return render_template('blog_detail.html', post={
            'id': p['id'], 'title': p.get(f'title_{lang}', p['title_es']), 'date': p['date'],
            'author': p['author'], 'image': p['image'], 'content': p.get(f'content_{lang}', p['content_es'])
        }, cart_count=get_cart_count())

    # ==========================================
    # 🛒 CARRITO UNIFICADO
    # ==========================================
    @app.route('/cart')
    def cart():
        if 'user_id' not in session:
            session['user_id'] = 999
        
        db_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        acc_items = session.get('acc_cart', [])
        
        unified_cart = []
        total = 0

        for i in db_items:
            subtotal = i.service.price * i.quantity
            unified_cart.append({
                'type': '🛠️ Servicio',
                'name': i.service.name_es,
                'price': i.service.price,
                'qty': i.quantity,
                'subtotal': subtotal,
                'remove_url': url_for('remove_from_cart', item_id=i.id)
            })
            total += subtotal

        for idx, i in enumerate(acc_items):
            subtotal = i['price'] * i['qty']
            unified_cart.append({
                'type': '📦 Accesorio',
                'name': i['name'],
                'price': i['price'],
                'qty': i['qty'],
                'subtotal': subtotal,
                'remove_url': url_for('remove_accessory_from_cart', idx=idx)
            })
            total += subtotal

        return render_template('cart.html', cart=unified_cart, total=total, cart_count=get_cart_count())

    @app.route('/add_to_cart/<int:service_id>', methods=['POST'])
    def add_to_cart(service_id):
        if 'user_id' not in session:
            session['user_id'] = 999
        item = CartItem.query.filter_by(user_id=session['user_id'], service_id=service_id).first()
        if item:
            item.quantity += 1
        else:
            db.session.add(CartItem(user_id=session['user_id'], service_id=service_id, quantity=1))
        db.session.commit()
        flash('✅ Agregado al carrito', 'success')
        return redirect(request.referrer or url_for('index'))

    @app.route('/remove_from_cart/<int:item_id>')
    def remove_from_cart(item_id):
        db.session.delete(CartItem.query.get_or_404(item_id))
        db.session.commit()
        flash('🗑️ Eliminado del carrito', 'warning')
        return redirect(url_for('cart'))

    @app.route('/add_accessory_to_cart/<int:accessory_id>', methods=['POST'])
    def add_accessory_to_cart(accessory_id):
        if 'acc_cart' not in session:
            session['acc_cart'] = []
        acc = None
        for cat in ACCESSORIES_DB.values():
            for item in cat:
                if item['id'] == accessory_id:
                    acc = item
                    break
        if not acc:
            return redirect(request.referrer or url_for('index'))
        
        cart = session['acc_cart']
        found = False
        for i in cart:
            if i['id'] == accessory_id:
                i['qty'] += 1
                found = True
                break
        if not found:
            cart.append({'id': acc['id'], 'name': acc['name'], 'price': acc['price'], 'image': acc['image'], 'qty': 1})
        
        session['acc_cart'] = cart
        flash('✅ Accesorio agregado al carrito', 'success')
        return redirect(request.referrer or url_for('accessories'))

    @app.route('/remove_accessory_from_cart/<int:idx>')
    def remove_accessory_from_cart(idx):
        if 'acc_cart' in session:
            session['acc_cart'].pop(idx, None)
        return redirect(url_for('cart'))

    # ==========================================
    # 💳 CHECKOUT CON MERCADOPAGO
    # ==========================================
    @app.route('/checkout', methods=['POST'])
    def checkout():
        if 'user_id' not in session:
            session['user_id'] = 999
        
        db_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        acc_items = session.get('acc_cart', [])
        
        if not db_items and not acc_items:
            flash('Tu carrito está vacío', 'warning')
            return redirect(url_for('cart'))
        
        total = sum(i.service.price * i.quantity for i in db_items) + sum(i['price'] * i['qty'] for i in acc_items)
        payment_method = request.form.get('payment_method', 'cash')
        
        if payment_method in ['pix', 'card']:
            mp = mercadopago.SDK("APP_USR-8016519599774599-052509-476af295380f4fe8d4546b997758c037-3423924992")
            
            items = []
            for i in db_items:
                items.append({"title": i.service.name_es, "unit_price": float(i.service.price), "quantity": i.quantity})
            for i in acc_items:
                items.append({"title": i['name'], "unit_price": float(i['price']), "quantity": i['qty']})
            
            # URLs absolutas
            back_urls = {
                "success": "http://localhost:5001/checkout/success",
                "failure": "http://localhost:5001/cart",
                "pending": "http://localhost:5001/cart"
            }
            
            # 🔥 FIX: Sin auto_return para evitar error 400
            preference_data = {
                "items": items,
                "currency_id": "BRL",
                "back_urls": back_urls
            }
            
            try:
                mp_response = mp.preference().create(preference_data)
                
                if mp_response.get("status") == 201 and "response" in mp_response:
                    init_point = mp_response["response"].get("init_point")
                    if init_point:
                        order_id = int(datetime.now().timestamp())
                        session['last_order'] = {
                            'id': order_id, 'items': items, 'total': total,
                            'payment': payment_method, 'date': datetime.now().strftime('%d/%m/%Y %H:%M')
                        }
                        for item in db_items: db.session.delete(item)
                        db.session.commit()
                        session.pop('acc_cart', None)
                        return redirect(init_point)
                
                flash(f"❌ Error MP: {mp_response.get('response', 'Desconocido')}", "error")
                return redirect(url_for('cart'))
                
            except Exception as e:
                flash(f"⚠️ Excepción: {str(e)}", "error")
                return redirect(url_for('cart'))
            else:
                order_id = int(datetime.now().timestamp())
            session['last_order'] = {
                'id': order_id, 'items': [], 'total': total,
                'payment': payment_method, 'date': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            for item in db_items: db.session.delete(item)
            db.session.commit()
            session.pop('acc_cart', None)
            return redirect(url_for('checkout_success'))

    @app.route('/checkout/success')
    def checkout_success():
        order = session.get('last_order')
        if not order:
            flash('No se encontró información de la compra. Intenta de nuevo.', 'warning')
            return redirect(url_for('index'))
        return render_template('checkout_success.html', order=order, cart_count=get_cart_count())

    @app.route('/invoice/<int:order_id>')
    def invoice(order_id):
        order = session.get('last_order')
        if not order or order['id'] != order_id:
            flash('Factura no disponible', 'warning')
            return redirect(url_for('index'))
        
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 18)
            pdf.cell(0, 10, "FACTURA SAVALATECH", ln=True, align="C")
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(0, 6, f"N° Orden: #{order['id']}", ln=True)
            pdf.cell(0, 6, f"Fecha: {order['date']}", ln=True)
            pdf.cell(0, 6, f"Método de Pago: {order['payment'].upper()}", ln=True)
            pdf.ln(8)
            
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "Detalle de la Compra", ln=True)
            pdf.set_font("Helvetica", "", 10)
            
            for item in order['items']:
                pdf.cell(120, 6, f"{item['name']} x{item['qty']}", 0)
                pdf.cell(40, 6, f"R$ {item['price']*item['qty']:.2f}", 0, 1, "R")
            
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, f"TOTAL: R$ {order['total']:.2f}", 1, 1, "R")
            pdf.ln(10)
            pdf.set_font("Helvetica", "I", 9)
            pdf.cell(0, 5, "Gracias por confiar en SavalaTech", ln=True, align="C")
            pdf.cell(0, 5, "www.savalatech.com | info@savalatech.com", ln=True, align="C")
            
            pdf_bytes = pdf.output(dest='S').encode('latin1')
            return send_file(
                io.BytesIO(pdf_bytes),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'Factura_SavalaTech_{order_id}.pdf'
            )
        except Exception as e:
            flash(f"Error al generar PDF: {str(e)}", "error")
            return redirect(url_for('checkout_success'))

    # ==========================================
    # 🔐 PANEL ADMIN
    # ==========================================
    @app.route('/admin')
    def admin_login():
        if session.get('admin_logged_in'):
            return redirect(url_for('admin_dashboard'))
        return render_template('admin/login.html')
    
    @app.route('/admin/login', methods=['POST'])
    def admin_do_login():
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'savalatech2026':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Credenciales incorrectas')
        return redirect(url_for('admin_login'))
    
    @app.route('/admin/dashboard')
    def admin_dashboard():
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        services = Service.query.all()
        orders = []
        return render_template('admin/dashboard.html', services=services, orders=orders)
    
    @app.route('/admin/add_service', methods=['POST'])
    def admin_add_service():
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        
        new_service = Service(
            name_es=request.form.get('name_es'),
            name_pt=request.form.get('name_pt'),
            description_es=request.form.get('description_es'),
            description_pt=request.form.get('description_es'),
            price=int(request.form.get('price')),
            category=request.form.get('category'),
            duration_hours=int(request.form.get('duration_hours')),
            image_url=request.form.get('image_url') or '/static/img/servicio-default.jpg'
        )
        db.session.add(new_service)
        db.session.commit()
        flash('✅ Servicio agregado', 'success')
        return redirect(url_for('admin_dashboard'))
    
    @app.route('/admin/delete_service/<int:service_id>')
    def admin_delete_service(service_id):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        flash('🗑️ Servicio eliminado', 'warning')
        return redirect(url_for('admin_dashboard'))
    
    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        return redirect(url_for('index'))

    def get_cart_count():
        count = 0
        if 'user_id' in session:
            count += sum(i.quantity for i in CartItem.query.filter_by(user_id=session['user_id']).all())
        if 'acc_cart' in session:
            count += sum(i['qty'] for i in session['acc_cart'])
        return count

    # INICIALIZAR BD
    with app.app_context():
        db.create_all()
        if Service.query.count() == 0:
            services = [
                Service(name_es="Mantenimiento Preventivo PC", name_pt="Manutenção Preventiva PC", 
                        description_es="Limpieza interna, cambio de pasta térmica, optimización", 
                        description_pt="Limpeza interna, troca de pasta térmica, otimização", 
                        price=180.00, category="computer", duration_hours=2, 
                        image_url="/static/img/servicio-mantenimiento.jpg"),
                Service(name_es="Reparación de Hardware", name_pt="Reparo de Hardware", 
                        description_es="Diagnóstico y reparación de componentes dañados", 
                        description_pt="Diagnóstico e reparo de componentes danificados", 
                        price=250.00, category="computer", duration_hours=3, 
                        image_url="/static/img/servicio-hardware.jpg"),
                Service(name_es="Instalación de Software", name_pt="Instalação de Software", 
                        description_es="Sistema operativo, drivers, programas esenciales", 
                        description_pt="Sistema operacional, drivers, programas essenciais", 
                        price=120.00, category="computer", duration_hours=2, 
                        image_url="/static/img/servicio-software.jpg"),
                Service(name_es="Mantenimiento Notebook", name_pt="Manutenção Notebook", 
                        description_es="Limpieza profunda, revisión de ventiladores", 
                        description_pt="Limpeza profunda, revisão de ventiladores", 
                        price=200.00, category="notebook", duration_hours=2, 
                        image_url="/static/img/servicio-notebook.jpg"),
                Service(name_es="Cambio de Pantalla", name_pt="Troca de Tela", 
                        description_es="Reemplazo de pantalla LCD/LED dañada", 
                        description_pt="Substituição de tela LCD/LED danificada", 
                        price=600.00, category="notebook", duration_hours=1, 
                        image_url="/static/img/servicio-pantalla.jpg"),
                Service(name_es="Recuperación de Datos", name_pt="Recuperação de Dados", 
                        description_es="Rescate de información de discos dañados", 
                        description_pt="Resgate de informações de discos danificados", 
                        price=400.00, category="computer", duration_hours=4, 
                        image_url="/static/img/servicio-datos.jpg"),
            ]
            db.session.add_all(services)
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 SavalaTech corriendo en http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)