document.addEventListener('DOMContentLoaded', function() {

    // Función helper para formatear precios en COP
    const formatCOP = (value) => {
        const num = parseInt(parseFloat(value));
        return `$ ${new Intl.NumberFormat('es-CO').format(num)} COP`;
    };

    // Función para actualizar el estado de los botones +/- según cantidad y stock
    const updateButtonStates = (itemId, quantity, stock) => {
        const decreaseBtn = document.getElementById(`btn-decrease-${itemId}`);
        const increaseBtn = document.getElementById(`btn-increase-${itemId}`);
        if (decreaseBtn) decreaseBtn.disabled = (quantity <= 1);
        if (increaseBtn) increaseBtn.disabled = (quantity >= stock);
    };

    // Al cargar, inicializar estado de botones de cada ítem
    document.querySelectorAll('.cart-item').forEach(item => {
        const itemId = item.id.replace('cart-item-', '');
        const stock = parseInt(item.dataset.stock);
        const quantityEl = document.getElementById(`item-quantity-${itemId}`);
        if (quantityEl) {
            updateButtonStates(itemId, parseInt(quantityEl.textContent), stock);
        }
    });


    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const productId = this.dataset.productId;
            const quantity = document.querySelector(`#quantity-${productId}`)
                ? parseInt(document.querySelector(`#quantity-${productId}`).value)
                : 1;

            fetch(`/cart/add/${productId}/?quantity=${quantity}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar contador del carrito
                    document.getElementById('cart-items-count').textContent = data.cart_items_count;

                    // Color del toast según si se llegó al tope
                    const toastColor = data.capped
                        ? "linear-gradient(to right, #e67e22, #e74c3c)"
                        : "linear-gradient(to right, #0063e6, #e60048)";

                    // Mostrar notificación
                    Toastify({
                        text: data.message,
                        duration: 3500,
                        gravity: "top",
                        position: "right",
                        backgroundColor: toastColor,
                        stopOnFocus: true,
                    }).showToast();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Funcionalidad para actualizar cantidades en el carrito
    const cartItemControls = document.querySelectorAll('.cart-item-control');

    cartItemControls.forEach(control => {
        control.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            const action = this.dataset.action;

            fetch('/cart/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    item_id: itemId,
                    action: action
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar contador del carrito
                    document.getElementById('cart-items-count').textContent = data.cart_items_count;

                    // Si el elemento fue eliminado
                    if (data.removed) {
                        const cartItem = document.getElementById(`cart-item-${itemId}`);
                        if (cartItem) {
                            cartItem.remove();
                        }
                    } else {
                        // Actualizar cantidad y total del item
                        const newQty = parseInt(data.quantity);
                        document.getElementById(`item-quantity-${itemId}`).textContent = newQty;
                        document.getElementById(`item-total-${itemId}`).textContent = formatCOP(data.item_total);

                        // Actualizar botones según nueva cantidad y stock del producto
                        const cartItemEl = document.getElementById(`cart-item-${itemId}`);
                        const stock = parseInt(cartItemEl.dataset.stock);
                        updateButtonStates(itemId, newQty, stock);
                    }

                    // Actualizar el total del carrito
                    document.getElementById('cart-total').textContent = formatCOP(data.cart_total);
                    const cartFinalTotal = document.getElementById('cart-final-total');
                    if(cartFinalTotal) cartFinalTotal.textContent = formatCOP(data.cart_total);

                    // Si el carrito está vacío después de eliminar todo
                    if (data.cart_items_count === 0) {
                        document.getElementById('cart-items').innerHTML = '<div class="alert alert-info">Tu carrito está vacío</div>';
                        document.getElementById('checkout-btn').classList.add('disabled');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});