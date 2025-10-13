from flask import Flask, render_template, request, jsonify

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Catálogo de productos (10 productos: 5 relojes de lujo y 5 joyas)
# Cada producto tiene un ID, nombre, categoría, precio, descripción e imagen
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

@app.route('/')
def index():
    """
    Página principal con el catálogo completo de productos.
    Permite filtrar por categoría y realizar búsquedas por nombre o descripción.
    """
    category = request.args.get('category', 'all')  # Categoría seleccionada (por defecto: 'all')
    search_query = request.args.get('search', '').lower()  # Término de búsqueda (por defecto: vacío)
    
    # Filtrar productos según la categoría y el término de búsqueda
    filtered_products = products
    if category != 'all':
        filtered_products = [p for p in filtered_products if p['category'] == category]
    if search_query:
        filtered_products = [p for p in filtered_products 
                           if search_query in p['name'].lower() or 
                           search_query in p['description'].lower()]
    
    # Renderizar la plantilla HTML con los productos filtrados
    return render_template('index.html', 
                         products=filtered_products, 
                         current_category=category,
                         search_query=search_query if search_query else '')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    Página de detalle de un producto específico.
    Muestra información detallada del producto seleccionado.
    """
    product = next((p for p in products if p['id'] == product_id), None)  # Buscar producto por ID
    if product:
        return render_template('product_detail.html', product=product)  # Renderizar plantilla con el producto
    return "Producto no encontrado", 404  # Mostrar error si el producto no existe

@app.route('/api/search')
def api_search():
    """
    API endpoint para realizar búsquedas dinámicas.
    Devuelve una lista de productos que coinciden con la categoría y el término de búsqueda.
    """
    query = request.args.get('q', '').lower()  # Término de búsqueda
    category = request.args.get('category', 'all')  # Categoría seleccionada
    
    # Filtrar productos según la categoría y el término de búsqueda
    filtered = products
    if category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
    if query:
        filtered = [p for p in filtered 
                   if query in p['name'].lower() or query in p['description'].lower()]
    
    return jsonify(filtered)  # Devolver los productos filtrados en formato JSON

if __name__ == '__main__':
    # Ejecutar la aplicación en modo de producción
    app.run(debug=False, host='0.0.0.0', port=5000)
