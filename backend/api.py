"""
Backend API for the luxury e-commerce application
Provides RESTful endpoints for product catalog
"""
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'
    }), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    try:
        category = request.args.get('category', 'all')
        search_query = request.args.get('search', '').lower()
        
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
        
        return jsonify({
            'success': True,
            'data': filtered_products,
            'count': len(filtered_products)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        product = next((p for p in products if p['id'] == product_id), None)
        
        if product:
            return jsonify({
                'success': True,
                'data': product
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get available product categories"""
    categories = [
        {'id': 'all', 'name': 'Todos los Productos', 'icon': '🏆'},
        {'id': 'watch', 'name': 'Relojes de Lujo', 'icon': '⌚'},
        {'id': 'jewelry', 'name': 'Joyas Exclusivas', 'icon': '💎'}
    ]
    return jsonify({
        'success': True,
        'data': categories
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
