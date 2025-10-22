from flask import Flask, render_template, request, jsonify
from typing import List, Dict, Optional

app = Flask(__name__)

# Catálogo de productos (10 productos: 5 relojes de lujo y 5 joyas)
# Using a list for ordering, but will create a dict for fast lookups
products_list = [
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

# Create a dictionary for O(1) product lookups by ID
products_dict = {product['id']: product for product in products_list}

def filter_products(products: List[Dict], category: str = 'all', search_query: str = '') -> List[Dict]:
    """
    Filter products by category and search query efficiently.
    
    Args:
        products: List of product dictionaries
        category: Category filter ('all', 'watch', 'jewelry')
        search_query: Search term to match in name or description
    
    Returns:
        Filtered list of products
    """
    filtered = products
    
    # Apply category filter if specified
    if category and category != 'all':
        filtered = [p for p in filtered if p.get('category') == category]
    
    # Apply search filter if specified (strip whitespace first)
    search_query = search_query.strip()
    if search_query:
        search_lower = search_query.lower()
        filtered = [
            p for p in filtered 
            if search_lower in p.get('name', '').lower() 
            or search_lower in p.get('description', '').lower()
        ]
    
    return filtered

@app.route('/')
def index():
    """Página principal con catálogo completo"""
    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '').strip()
    
    # Use optimized filter function
    filtered_products = filter_products(products_list, category, search_query)
    
    return render_template('index.html', 
                         products=filtered_products, 
                         current_category=category,
                         search_query=search_query)

@app.route('/product/<int:product_id>')
def product_detail(product_id: int):
    """Página de detalle del producto"""
    # Use dictionary for O(1) lookup instead of O(n) search
    product = products_dict.get(product_id)
    if product:
        return render_template('product_detail.html', product=product)
    return "Producto no encontrado", 404

@app.route('/api/search')
def api_search():
    """API endpoint para búsqueda dinámica"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', 'all')
    
    # Use optimized filter function
    filtered = filter_products(products_list, category, query)
    
    return jsonify(filtered)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
