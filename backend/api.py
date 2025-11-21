"""
Backend API for the luxury e-commerce application
Provides RESTful endpoints for product catalog with security features
"""
import logging
import os
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import bleach

# Initialize Flask app
app = Flask(__name__)

# Security configurations
# In production, JWT_SECRET_KEY MUST be set via environment variable
# The application will fail to start if not set in production mode
if os.environ.get('FLASK_ENV') == 'production' and not os.environ.get('JWT_SECRET_KEY'):
    raise RuntimeError("JWT_SECRET_KEY environment variable must be set in production mode")

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize security extensions
CORS(app)  # Enable CORS for frontend-backend communication
jwt = JWTManager(app)

# Rate limiting configuration
# Note: Using in-memory storage for development. In production, use Redis or database-backed storage
# to persist rate limits across application restarts. Example:
# storage_uri="redis://localhost:6379"
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# HTTPS enforcement and CSP (only in production)
if os.environ.get('FLASK_ENV') == 'production':
    Talisman(app, 
             force_https=True,
             strict_transport_security=True,
             content_security_policy={
                 'default-src': "'self'",
                 'script-src': "'self' 'unsafe-inline'",
                 'style-src': "'self' 'unsafe-inline'",
                 'img-src': "'self' https: data:",
                 'font-src': "'self'",
                 'connect-src': "'self'"
             })

# Configure audit logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('audit.log'),
        logging.StreamHandler()
    ]
)
audit_logger = logging.getLogger('audit')

def log_audit(action, details, user=None):
    """Log security and audit events"""
    remote_addr = request.remote_addr if request and hasattr(request, 'remote_addr') else 'N/A'
    user_info = user if user else 'anonymous'
    audit_logger.info(f"Action: {action} | User: {user_info} | Details: {details} | IP: {remote_addr}")

def sanitize_input(text, max_length=200):
    """Sanitize and validate user input"""
    if not text:
        return ""
    # Remove HTML tags and limit length
    sanitized = bleach.clean(str(text), tags=[], strip=True)
    return sanitized[:max_length]

def validate_category(category):
    """Validate category parameter"""
    valid_categories = ['all', 'watch', 'jewelry']
    sanitized = sanitize_input(category, max_length=20)
    return sanitized if sanitized in valid_categories else 'all'

# Product catalog data
products = [
    {
        'id': 1,
        'name': 'Rolex Submariner',
        'category': 'watch',
        'price': 12500.00,
        'description': 'Reloj de buceo icónico con bisel giratorio unidireccional y resistencia al agua de 300 metros.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Rolex+Submariner'
    },
    {
        'id': 2,
        'name': 'Patek Philippe Nautilus',
        'category': 'watch',
        'price': 35000.00,
        'description': 'Reloj deportivo elegante con caja de acero inoxidable y diseño portilla distintivo.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Patek+Philippe'
    },
    {
        'id': 3,
        'name': 'Audemars Piguet Royal Oak',
        'category': 'watch',
        'price': 28000.00,
        'description': 'Reloj de lujo con diseño octogonal característico y acabado "Tapisserie".',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=AP+Royal+Oak'
    },
    {
        'id': 4,
        'name': 'Omega Speedmaster',
        'category': 'watch',
        'price': 6500.00,
        'description': 'El legendario reloj lunar, el único certificado por la NASA para vuelos espaciales.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Omega+Speedmaster'
    },
    {
        'id': 5,
        'name': 'Cartier Santos',
        'category': 'watch',
        'price': 7200.00,
        'description': 'Reloj aviador clásico con tornillos visibles en el bisel y correa de cuero.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Cartier+Santos'
    },
    {
        'id': 6,
        'name': 'Collar de Diamantes',
        'category': 'jewelry',
        'price': 15000.00,
        'description': 'Elegante collar de diamantes de 18 quilates con piedras de corte brillante.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Diamond+Necklace'
    },
    {
        'id': 7,
        'name': 'Anillo de Compromiso',
        'category': 'jewelry',
        'price': 8500.00,
        'description': 'Anillo de compromiso con diamante central de 2 quilates y banda de oro blanco.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Engagement+Ring'
    },
    {
        'id': 8,
        'name': 'Brazalete de Oro',
        'category': 'jewelry',
        'price': 4200.00,
        'description': 'Brazalete de oro amarillo de 18k con diseño entrelazado y cierre de seguridad.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Gold+Bracelet'
    },
    {
        'id': 9,
        'name': 'Pendientes de Esmeralda',
        'category': 'jewelry',
        'price': 9800.00,
        'description': 'Pendientes de esmeralda colombiana con diamantes circundantes en oro blanco.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Emerald+Earrings'
    },
    {
        'id': 10,
        'name': 'Broche de Zafiro',
        'category': 'jewelry',
        'price': 6700.00,
        'description': 'Broche de zafiro azul con diseño de flor y detalles de diamantes.',
        'image': 'https://via.placeholder.com/400x400/000000/FFD700?text=Sapphire+Brooch'
    }
]

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Login endpoint to obtain JWT token"""
    try:
        data = request.get_json(silent=True)
        if not data:
            log_audit('LOGIN_FAILED', 'No data provided')
            return jsonify({
                'success': False,
                'error': 'Invalid request data'
            }), 400
        
        username = sanitize_input(data.get('username', ''), max_length=50)
        # Validate password length to prevent resource exhaustion
        password = data.get('password', '')
        if len(password) > 200:
            log_audit('LOGIN_FAILED', 'Password too long')
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        if not username or not password:
            log_audit('LOGIN_FAILED', f'Missing credentials for user: {username}')
            return jsonify({
                'success': False,
                'error': 'Username and password are required'
            }), 400
        
        # Get demo credentials from environment variables (with defaults for development only)
        demo_username = os.environ.get('DEMO_USERNAME', 'admin')
        demo_password = os.environ.get('DEMO_PASSWORD', 'admin123')
        
        # Simple authentication (in production, use a proper authentication system)
        if username == demo_username and password == demo_password:
            access_token = create_access_token(identity=username)
            log_audit('LOGIN_SUCCESS', f'User logged in: {username}', user=username)
            return jsonify({
                'success': True,
                'access_token': access_token,
                'token_type': 'Bearer'
            }), 200
        else:
            log_audit('LOGIN_FAILED', f'Invalid credentials for user: {username}')
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
    except Exception as e:
        app.logger.error('Login error', exc_info=True)
        log_audit('LOGIN_ERROR', str(e))
        return jsonify({
            'success': False,
            'error': 'Internal server error during login'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    log_audit('HEALTH_CHECK', 'Health check performed')
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'security': 'enabled'
    }), 200

@app.route('/api/products', methods=['GET'])
@limiter.limit("100 per minute")
def get_products():
    """Get all products with optional filtering"""
    try:
        # Validate and sanitize input parameters
        category = validate_category(request.args.get('category', 'all'))
        search_query = sanitize_input(request.args.get('search', ''), max_length=100).lower()
        
        # Filter products
        filtered_products = products
        
        if category != 'all':
            filtered_products = [p for p in filtered_products if p['category'] == category]
        
        if search_query:
            filtered_products = [
                p for p in filtered_products 
                if search_query in p['name'].lower() or 
                search_query in p['description'].lower()
            ]
        
        log_audit('GET_PRODUCTS', f'Category: {category}, Search: {search_query}, Results: {len(filtered_products)}')
        
        return jsonify({
            'success': True,
            'data': filtered_products,
            'count': len(filtered_products)
        }), 200
    except Exception:
        # Log the error internally but don't expose stack trace
        app.logger.error('Error fetching products', exc_info=True)
        log_audit('GET_PRODUCTS_ERROR', 'Internal server error')
        return jsonify({
            'success': False,
            'error': 'Internal server error while fetching products'
        }), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
@limiter.limit("100 per minute")
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        # Validate product_id is positive integer
        if product_id <= 0:
            log_audit('GET_PRODUCT_INVALID', f'Invalid product ID: {product_id}')
            return jsonify({
                'success': False,
                'error': 'Invalid product ID'
            }), 400
            
        product = next((p for p in products if p['id'] == product_id), None)
        
        if product:
            log_audit('GET_PRODUCT', f'Product ID: {product_id}')
            return jsonify({
                'success': True,
                'data': product
            }), 200
        else:
            log_audit('GET_PRODUCT_NOT_FOUND', f'Product ID: {product_id}')
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404
    except Exception:
        # Log the error internally but don't expose stack trace
        app.logger.error('Error fetching product by ID', exc_info=True)
        log_audit('GET_PRODUCT_ERROR', f'Product ID: {product_id}')
        return jsonify({
            'success': False,
            'error': 'Internal server error while fetching product'
        }), 500

@app.route('/api/categories', methods=['GET'])
@limiter.limit("100 per minute")
def get_categories():
    """Get available product categories"""
    categories = [
        {'id': 'all', 'name': 'Todos los Productos', 'icon': '🏆'},
        {'id': 'watch', 'name': 'Relojes de Lujo', 'icon': '⌚'},
        {'id': 'jewelry', 'name': 'Joyas Exclusivas', 'icon': '💎'}
    ]
    log_audit('GET_CATEGORIES', 'Categories retrieved')
    return jsonify({
        'success': True,
        'data': categories
    }), 200

@app.route('/api/admin/products', methods=['GET'])
@jwt_required()
@limiter.limit("50 per minute")
def get_admin_products():
    """Protected endpoint for admin access to products"""
    try:
        current_user = get_jwt_identity()
        log_audit('ADMIN_GET_PRODUCTS', f'Admin access', user=current_user)
        
        return jsonify({
            'success': True,
            'data': products,
            'count': len(products),
            'user': current_user
        }), 200
    except Exception:
        app.logger.error('Error in admin products endpoint', exc_info=True)
        log_audit('ADMIN_GET_PRODUCTS_ERROR', 'Internal server error')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    log_audit('404_ERROR', f'Endpoint not found: {request.path}')
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    log_audit('500_ERROR', 'Internal server error')
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors"""
    log_audit('RATE_LIMIT_EXCEEDED', f'Rate limit exceeded: {request.path}')
    return jsonify({
        'success': False,
        'error': 'Rate limit exceeded. Please try again later.'
    }), 429

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
