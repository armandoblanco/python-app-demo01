/**
 * Configuration file for the frontend application
 */

const CONFIG = {
    // API base URL - can be changed based on environment
    API_BASE_URL: 'http://localhost:5000',
    
    // API endpoints
    ENDPOINTS: {
        HEALTH: '/api/health',
        PRODUCTS: '/api/products',
        PRODUCT_BY_ID: '/api/products/{id}',
        CATEGORIES: '/api/categories'
    },
    
    // Request timeout in milliseconds
    REQUEST_TIMEOUT: 10000,
    
    // Debounce delay for search (milliseconds)
    SEARCH_DEBOUNCE: 500
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}
