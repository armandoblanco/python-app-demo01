/**
 * Product detail page logic
 */

/**
 * Get product ID from URL
 */
function getProductIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/**
 * Initialize product detail page
 */
async function init() {
    const productId = getProductIdFromURL();
    
    if (!productId) {
        showError('ID de producto no válido');
        return;
    }
    
    try {
        // Check API health
        await api.healthCheck();
        
        // Load product details
        await loadProductDetail(productId);
    } catch (error) {
        console.error('Initialization failed:', error);
        showError('Error al conectar con el servidor. Por favor, intenta más tarde.');
    }
}

/**
 * Load and render product details
 */
async function loadProductDetail(productId) {
    const productDetail = document.getElementById('productDetail');
    productDetail.innerHTML = '<div class="loading">Cargando producto...</div>';
    
    try {
        const response = await api.getProduct(productId);
        const product = response.data;
        
        // Update page title
        document.title = `${product.name} - Luxury Collection`;
        
        // Render product details
        productDetail.innerHTML = `
            <div class="product-detail">
                <div class="product-image-container">
                    <img src="${product.image}" alt="${product.name}" class="product-image">
                </div>

                <div class="product-info">
                    <span class="product-category">
                        ${product.category === 'watch' ? '⌚ RELOJ DE LUJO' : '💎 JOYERÍA EXCLUSIVA'}
                    </span>

                    <h2 class="product-name">${product.name}</h2>

                    <div class="product-price">
                        <span class="price-label">PRECIO EN USD</span>
                        $${formatPrice(product.price)}
                    </div>

                    <div class="product-description">
                        <p>${product.description}</p>
                    </div>

                    <div class="product-features">
                        <h3>Características Destacadas</h3>
                        <ul>
                            ${getFeatures(product.category).map(feature => `
                                <li>${feature}</li>
                            `).join('')}
                        </ul>
                    </div>

                    <div class="action-buttons">
                        <button class="btn btn-primary" onclick="addToCart()">
                            🛒 Agregar al Carrito
                        </button>
                        <button class="btn btn-secondary" onclick="contactUs()">
                            💬 Consultar
                        </button>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Failed to load product:', error);
        showError('Error al cargar el producto. Por favor, intenta más tarde.');
    }
}

/**
 * Get features based on category
 */
function getFeatures(category) {
    if (category === 'watch') {
        return [
            'Mecanismo de precisión suiza',
            'Cristal de zafiro resistente a rayones',
            'Resistencia al agua',
            'Garantía internacional de 2 años',
            'Caja de presentación de lujo incluida'
        ];
    } else {
        return [
            'Materiales de la más alta calidad',
            'Certificado de autenticidad',
            'Diseño exclusivo y único',
            'Garantía de por vida',
            'Estuche de presentación elegante'
        ];
    }
}

/**
 * Format price with thousands separator
 */
function formatPrice(price) {
    return price.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Show error message
 */
function showError(message) {
    const productDetail = document.getElementById('productDetail');
    productDetail.innerHTML = `
        <div class="error">
            <p>${message}</p>
        </div>
    `;
}

/**
 * Add to cart (demo function)
 */
function addToCart() {
    alert('Función de compra no implementada en esta demo');
}

/**
 * Contact us (demo function)
 */
function contactUs() {
    alert('Función de consulta no implementada en esta demo');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
