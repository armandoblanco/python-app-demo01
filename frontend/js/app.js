/**
 * Main application logic for the catalog page
 */

// State management
let currentCategory = 'all';
let currentSearch = '';
let searchTimeout;

/**
 * Initialize the application
 */
async function init() {
    try {
        // Check API health
        await api.healthCheck();
        
        // Load categories
        await loadCategories();
        
        // Load products
        await loadProducts();
        
        // Setup event listeners
        setupEventListeners();
    } catch (error) {
        console.error('Initialization failed:', error);
        showError('Error al conectar con el servidor. Por favor, intenta más tarde.');
    }
}

/**
 * Load and render categories
 */
async function loadCategories() {
    try {
        const response = await api.getCategories();
        const categories = response.data;
        
        const filterButtons = document.getElementById('filterButtons');
        filterButtons.innerHTML = categories.map(category => `
            <button class="filter-btn ${category.id === currentCategory ? 'active' : ''}" 
                    data-category="${category.id}">
                ${category.icon} ${category.name}
            </button>
        `).join('');
        
        // Add click listeners to category buttons
        filterButtons.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                currentCategory = btn.dataset.category;
                loadProducts();
            });
        });
    } catch (error) {
        console.error('Failed to load categories:', error);
    }
}

/**
 * Load and render products
 */
async function loadProducts() {
    const productsGrid = document.getElementById('productsGrid');
    productsGrid.innerHTML = '<div class="loading">Cargando productos...</div>';
    
    try {
        const response = await api.getProducts({
            category: currentCategory,
            search: currentSearch
        });
        
        const products = response.data;
        
        if (products.length === 0) {
            productsGrid.innerHTML = `
                <div class="no-results">
                    <p>No se encontraron productos que coincidan con tu búsqueda.</p>
                    <p style="font-size: 0.8em; margin-top: 20px; color: #ffffff;">
                        Intenta con otros términos o explora todas las categorías.
                    </p>
                </div>
            `;
            return;
        }
        
        productsGrid.innerHTML = products.map(product => `
            <a href="product.html?id=${product.id}" class="product-card">
                <img src="${product.image}" alt="${product.name}" class="product-image">
                <span class="product-category">
                    ${product.category === 'watch' ? '⌚ Reloj' : '💎 Joya'}
                </span>
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <p class="product-price">
                    <span class="price-label">USD</span> $${formatPrice(product.price)}
                </p>
            </a>
        `).join('');
        
        // Update filter button states
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.category === currentCategory);
        });
    } catch (error) {
        console.error('Failed to load products:', error);
        showError('Error al cargar los productos. Por favor, intenta más tarde.');
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    const searchBox = document.getElementById('searchBox');
    
    searchBox.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            currentSearch = e.target.value.trim();
            loadProducts();
        }, CONFIG.SEARCH_DEBOUNCE);
    });
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
    const productsGrid = document.getElementById('productsGrid');
    productsGrid.innerHTML = `
        <div class="error">
            <p>${message}</p>
        </div>
    `;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
