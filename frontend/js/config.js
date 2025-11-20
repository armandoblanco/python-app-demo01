/**
 * Configuration file for the frontend application
 * Supports both Python/Flask and PHP backends
 */

const CONFIG = {
    // Backend type: 'python' or 'php'
    // Change this to switch between backends
    BACKEND_TYPE: 'php', // Default to PHP backend
    
    // Backend configurations
    BACKENDS: {
        python: {
            API_BASE_URL: 'http://localhost:5000',
            ENDPOINTS: {
                HEALTH: '/api/health',
                PRODUCTS: '/api/products',
                PRODUCT_BY_ID: '/api/products/{id}',
                CATEGORIES: '/api/categories'
            }
        },
        php: {
            API_BASE_URL: 'http://localhost:8080',
            ENDPOINTS: {
                HEALTH: '/api/health.php',
                PRODUCTS: '/api/products.php',
                PRODUCT_BY_ID: '/api/product.php?id={id}',
                CATEGORIES: '/api/categories.php'
            }
        }
    },
    
    // Request timeout in milliseconds
    REQUEST_TIMEOUT: 10000,
    
    // Debounce delay for search (milliseconds)
    SEARCH_DEBOUNCE: 500,
    
    // Get current backend configuration
    get API_BASE_URL() {
        return this.BACKENDS[this.BACKEND_TYPE].API_BASE_URL;
    },
    
    get ENDPOINTS() {
        return this.BACKENDS[this.BACKEND_TYPE].ENDPOINTS;
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
