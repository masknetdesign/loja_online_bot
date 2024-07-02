document.addEventListener('DOMContentLoaded', () => {
    const products = [
        { id: 'prod1', name: 'Produto 1', price: 10.00 },
        { id: 'prod2', name: 'Produto 2', price: 20.00 },
        { id: 'prod3', name: 'Produto 3', price: 30.00 },
    ];

    const cart = [];

    const productsContainer = document.getElementById('products');
    const cartContainer = document.getElementById('cart');
    const checkoutButton = document.getElementById('checkout');

    function renderProducts() {
        productsContainer.innerHTML = '';
        products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.className = 'product';
            productElement.innerHTML = `
                <h3>${product.name}</h3>
                <p>R$ ${product.price.toFixed(2)}</p>
                <button onclick="addToCart('${product.id}')">Adicionar ao Carrinho</button>
            `;
            productsContainer.appendChild(productElement);
        });
    }

    window.addToCart = function (productId) {
        const product = products.find(p => p.id === productId);
        cart.push(product);
        renderCart();
    }

    function renderCart() {
        cartContainer.innerHTML = '';
        cart.forEach((item, index) => {
            const cartItem = document.createElement('li');
            cartItem.textContent = `${item.name} - R$ ${item.price.toFixed(2)}`;
            cartContainer.appendChild(cartItem);
        });
    }

    checkoutButton.addEventListener('click', () => {
        alert('Compra finalizada com sucesso!');
        cart.length = 0;  // Limpa o carrinho
        renderCart();
    });

    renderProducts();
});
