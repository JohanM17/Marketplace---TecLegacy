document.addEventListener('DOMContentLoaded', function () {

    // Función para formatear el precio (Moneda Colombiana)
    const formatCOP = (val) => {
        return `$ ${new Intl.NumberFormat('es-CO').format(parseInt(val || 0))} COP`;
    };

    /**
     * SISTEMA DE TRANSMISIÓN GLOBAL (Broadcasting)
     * Esta función "grita" a toda la página que el carrito ha cambiado.
     */
    const notifyCartUpdate = (count) => {
        const event = new CustomEvent('cart:updated', { detail: { count: count } });
        document.dispatchEvent(event);
    };

    /**
     * ESCUCHADOR INTELIGENTE
     * Todos los elementos con la clase .live-cart-count escuchan el "grito"
     * y se actualizan a sí mismos de forma independiente.
     */
    document.addEventListener('cart:updated', function (e) {
        const newCount = e.detail.count;
        const badges = document.querySelectorAll('.live-cart-count');

        badges.forEach(badge => {
            badge.textContent = newCount;

            // Animación PREMIUM de confirmación
            badge.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.3s';
            badge.style.transform = 'scale(1.4)';
            badge.style.backgroundColor = '#28a745'; // Breve destello verde de éxito

            setTimeout(() => {
                badge.style.transform = 'scale(1)';
                badge.style.backgroundColor = '#dc3545'; // Vuelve al rojo original
            }, 400);
        });

        // Actualizar el contador de la página de carrito si existe
        const pageCount = document.getElementById('cart-page-count');
        if (pageCount) pageCount.textContent = newCount;
    });

    // Función para botones +/- (Solo si estamos dentro de la página del carrito)
    const updateButtonStates = (itemId, qty, stock) => {
        const dBtn = document.getElementById(`btn-decrease-${itemId}`);
        const iBtn = document.getElementById(`btn-increase-${itemId}`);
        if (dBtn) dBtn.disabled = (qty <= 1);
        if (iBtn) iBtn.disabled = (qty >= stock);
    };

    // DELEGACIÓN DE EVENTOS (Captura clics en cualquier parte para mayor robustez)
    document.addEventListener('click', function (e) {

        // --- CASO 1: AÑADIR AL CARRITO ---
        const addBtn = e.target.closest('.add-to-cart-btn');
        if (addBtn) {
            e.preventDefault();
            const pId = addBtn.dataset.productId;
            const qInp = document.querySelector(`#quantity-${pId}`);
            const qty = qInp ? parseInt(qInp.value) : 1;

            fetch(`/cart/add/${pId}/?quantity=${qty}&ajax=1&_t=${new Date().getTime()}`, {
                method: 'GET',
                cache: 'no-store', // Fuerza al móvil a no usar datos viejos
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // NOTIFICAR EL CAMBIO A TODA LA PÁGINA
                        notifyCartUpdate(data.cart_items_count);

                        if (typeof Toastify !== 'undefined') {
                            Toastify({
                                text: data.message,
                                duration: 2500,
                                backgroundColor: data.capped ? "#ffc107" : "#0d6efd",
                                gravity: "bottom",
                                position: "center"
                            }).showToast();
                        }
                    }
                })
                .catch(err => console.error("Error en AJAX:", err));
        }

        // --- CASO 2: CONTROLES DENTRO DEL CARRITO ---
        const ctrlBtn = e.target.closest('.cart-item-control');
        if (ctrlBtn) {
            const iId = ctrlBtn.dataset.itemId;
            const act = ctrlBtn.dataset.action;

            fetch('/cart/update/?ajax=1', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': (typeof csrfToken !== 'undefined') ? csrfToken : ''
                },
                body: JSON.stringify({ item_id: iId, action: act })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // NOTIFICAR EL CAMBIO A TODA LA PÁGINA
                        notifyCartUpdate(data.cart_items_count);

                        if (data.removed) {
                            const itemRow = document.getElementById(`cart-item-${iId}`);
                            if (itemRow) itemRow.remove();
                        } else {
                            const qEl = document.getElementById(`item-quantity-${iId}`);
                            const tEl = document.getElementById(`item-total-${iId}`);
                            if (qEl) qEl.textContent = data.quantity;
                            if (tEl) tEl.textContent = formatCOP(data.item_total);

                            const itemDiv = document.getElementById(`cart-item-${iId}`);
                            if (itemDiv) updateButtonStates(iId, parseInt(data.quantity), parseInt(itemDiv.dataset.stock));
                        }

                        // Actualizar Totales Finales de la vista de carrito
                        const t1 = document.getElementById('cart-total');
                        const t2 = document.getElementById('cart-final-total');
                        if (t1) t1.textContent = formatCOP(data.cart_total);
                        if (t2) t2.textContent = formatCOP(data.cart_total);

                        if (data.cart_items_count === 0) window.location.reload();
                    }
                })
                .catch(err => console.error("Error al actualizar:", err));
        }
    });
});