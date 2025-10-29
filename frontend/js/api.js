/**
 * API client for backend communication
 */

class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    /**
     * Generic request method
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        // Setup timeout with AbortController
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.REQUEST_TIMEOUT);
        
        try {
            // Only set Content-Type for requests with body
            const headers = { ...options.headers };
            if (options.method && ['POST', 'PUT', 'PATCH'].includes(options.method.toUpperCase())) {
                headers['Content-Type'] = 'application/json';
            }
            
            const response = await fetch(url, {
                ...options,
                headers,
                signal: controller.signal
            });

            clearTimeout(timeoutId);
            
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            console.error('API request failed:', error);
            throw error;
        }
    }

    /**
     * Health check
     */
    async healthCheck() {
        return await this.request(CONFIG.ENDPOINTS.HEALTH);
    }

    /**
     * Get all products with optional filters
     */
    async getProducts(filters = {}) {
        const params = new URLSearchParams();
        
        if (filters.category && filters.category !== 'all') {
            params.append('category', filters.category);
        }
        
        if (filters.search) {
            params.append('search', filters.search);
        }

        const query = params.toString();
        const endpoint = query ? `${CONFIG.ENDPOINTS.PRODUCTS}?${query}` : CONFIG.ENDPOINTS.PRODUCTS;
        
        return await this.request(endpoint);
    }

    /**
     * Get a specific product by ID
     */
    async getProduct(productId) {
        const endpoint = CONFIG.ENDPOINTS.PRODUCT_BY_ID.replace('{id}', productId);
        return await this.request(endpoint);
    }

    /**
     * Get available categories
     */
    async getCategories() {
        return await this.request(CONFIG.ENDPOINTS.CATEGORIES);
    }
}

// Create global API client instance
const api = new APIClient(CONFIG.API_BASE_URL);
