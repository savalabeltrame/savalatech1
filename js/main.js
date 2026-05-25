// ==========================================
// SAVALATECH PRO - JAVASCRIPT
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    initSmoothScroll();
    initBackToTop();
    initToastNotifications();
    initLoadingButtons();
    initNewsletterValidation();
});

// 1. SCROLL SUAVE + BOTÓN VOLVER ARRIBA
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

function initBackToTop() {
    const btn = document.createElement('button');
    btn.id = 'backToTop';
    btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(btn);

    window.addEventListener('scroll', () => {
        btn.classList.toggle('visible', window.scrollY > 400);
    });

    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// 2. NOTIFICACIONES TOAST PROFESIONALES (Reemplaza los flash básicos)
function initToastNotifications() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);

    const flashes = document.querySelectorAll('.flash-message-data');
    flashes.forEach(el => {
        const msg = el.dataset.message;
        const type = el.dataset.category || 'success';
        showToast(msg, type);
        el.remove(); // Limpia del DOM después de leer
    });
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icons = { success: 'fa-check-circle', warning: 'fa-exclamation-triangle', error: 'fa-times-circle', info: 'fa-info-circle' };
    toast.innerHTML = `<i class="fas ${icons[type] || icons.info}"></i><span>${message}</span>`;
    
    container.appendChild(toast);
    
    // Auto-remove
    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// 3. ESTADOS DE CARGA EN BOTONES
function initLoadingButtons() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            if (btn && !btn.disabled) {
                btn.dataset.originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
                btn.disabled = true;
            }
        });
    });
}

// 4. VALIDACIÓN NEWSLETTER
function initNewsletterValidation() {
    const form = document.querySelector('.newsletter-form');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const input = this.querySelector('input[type="email"]');
        const email = input.value.trim();
        
        if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            showToast('Por favor ingresa un email válido', 'error');
            input.focus();
            return;
        }
        
        // Simulación de envío
        showToast('¡Suscripción exitosa! Recibirás nuestras novedades 📧', 'success');
        input.value = '';
    });
}

// Menú de idiomas (existente)
function toggleLangMenu() {
    document.getElementById('langDropdown').classList.toggle('show');
}

window.onclick = function(event) {
    if (!event.target.matches('.lang-btn') && !event.target.closest('.lang-btn')) {
        const dropdowns = document.getElementsByClassName('lang-dropdown');
        for (let i = 0; i < dropdowns.length; i++) dropdowns[i].classList.remove('show');
    }
}