"""
Aplicación Flask: E-commerce de Relojes de Lujo y Joyas
========================================================

Esta aplicación web implementa una tienda en línea básica con las siguientes funcionalidades:
- Catálogo de productos (relojes de lujo y joyas)
- Búsqueda de productos por nombre y descripción
- Filtrado por categoría (relojes o joyas)
- Página de detalle para cada producto
- API REST para búsqueda dinámica

Tecnologías utilizadas:
- Flask: Framework web minimalista para Python
- Jinja2: Motor de plantillas (incluido con Flask)
- HTML/CSS/JavaScript: Frontend con diseño responsive
"""

from flask import Flask, render_template, request, jsonify

# Crear una instancia de la aplicación Flask
# __name__ le indica a Flask dónde encontrar recursos (templates, static files)
app = Flask(__name__)

# ============================================================================
# DATOS DE PRODUCTOS - Almacenados en Memoria
# ============================================================================
# En una aplicación real, estos datos vendrían de una base de datos.
# Aquí usamos una lista de diccionarios Python para simplicidad.
#
# Estructura de cada producto:
# - id: Identificador único del producto (int)
# - name: Nombre del producto (string)
# - category: Tipo de producto - 'watch' (reloj) o 'jewelry' (joya)
# - price: Precio en USD (float)
# - description: Descripción detallada del producto (string)
# - image: URL de la imagen del producto (string - placeholder en este caso)
#
# Total: 10 productos (5 relojes de lujo + 5 joyas exclusivas)
# ============================================================================
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

# ============================================================================
# RUTAS (ENDPOINTS) DE LA APLICACIÓN
# ============================================================================
# Flask usa decoradores (@app.route) para definir qué función manejar
# cada URL. Cuando un usuario visita una URL, Flask ejecuta la función
# correspondiente y devuelve el resultado al navegador.
# ============================================================================

@app.route('/')
def index():
    """
    RUTA PRINCIPAL: Catálogo de productos con búsqueda y filtros
    ============================================================
    
    URL: http://localhost:5000/
    Método HTTP: GET
    
    Parámetros de URL opcionales:
    - category: Filtra por categoría ('all', 'watch', 'jewelry')
      Ejemplo: /?category=watch
    - search: Busca en nombre y descripción
      Ejemplo: /?search=rolex
    - Ambos: /?category=watch&search=rolex
    
    Proceso:
    1. Lee los parámetros de búsqueda de la URL
    2. Filtra los productos según categoría
    3. Filtra los productos según término de búsqueda
    4. Renderiza la plantilla HTML con los productos filtrados
    
    Retorna:
    - HTML renderizado con el catálogo de productos
    """
    # Paso 1: Obtener parámetros de la URL usando request.args
    # request.args.get() devuelve None si el parámetro no existe
    # El segundo argumento es el valor por defecto
    category = request.args.get('category', 'all')  # Categoría seleccionada (por defecto: 'all')
    search_query = request.args.get('search', '').lower()  # Término de búsqueda (por defecto: vacío, convertido a minúsculas)
    
    # Paso 2: Comenzar con todos los productos
    filtered_products = products
    
    # Paso 3: Aplicar filtro de categoría
    # Solo si el usuario seleccionó una categoría específica (no 'all')
    if category != 'all':
        # List comprehension: crea una nueva lista con solo los productos que cumplen la condición
        # Sintaxis: [elemento for elemento in lista if condición]
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    # Paso 4: Aplicar filtro de búsqueda
    # Solo si el usuario escribió algo en el cuadro de búsqueda
    if search_query:
        # Buscar el término tanto en el nombre como en la descripción
        # .lower() hace la búsqueda insensible a mayúsculas/minúsculas
        filtered_products = [p for p in filtered_products 
                           if search_query in p['name'].lower() or 
                           search_query in p['description'].lower()]
    
    # Paso 5: Renderizar la plantilla HTML con los datos filtrados
    # render_template() usa Jinja2 para reemplazar variables en el HTML
    # Las variables pasadas aquí estarán disponibles en el template como {{ variable }}
    return render_template('index.html', 
                         products=filtered_products,       # Lista de productos a mostrar
                         current_category=category,         # Categoría actual (para marcar botón activo)
                         search_query=search_query if search_query else '')  # Término de búsqueda (para mostrar en input)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    RUTA DE DETALLE: Muestra información detallada de un producto específico
    =========================================================================
    
    URL: http://localhost:5000/product/<id>
    Método HTTP: GET
    
    Parámetros de ruta:
    - product_id: ID del producto a mostrar (int)
      Ejemplo: /product/1 → muestra el producto con id=1
    
    El decorador <int:product_id> indica que:
    1. Este segmento de la URL debe ser un número entero
    2. Flask lo convertirá automáticamente a int
    3. Se pasará como argumento a la función
    
    Proceso:
    1. Busca el producto por ID en la lista de productos
    2. Si existe, renderiza la página de detalle
    3. Si no existe, devuelve error 404
    
    Retorna:
    - HTML con los detalles del producto, o
    - Error 404 si el producto no existe
    """
    # Buscar producto por ID usando la función next() y un generador
    # next(iterador, valor_por_defecto) devuelve el primer elemento que cumple la condición
    # Si no encuentra ninguno, devuelve el valor por defecto (None en este caso)
    # 
    # Esto es más eficiente que filtrar toda la lista porque se detiene
    # en cuanto encuentra el primer producto con el ID buscado
    product = next((p for p in products if p['id'] == product_id), None)
    
    # Verificar si se encontró el producto
    if product:
        # Si existe: renderizar plantilla con los datos del producto
        return render_template('product_detail.html', product=product)
    
    # Si no existe: devolver mensaje de error con código HTTP 404
    # El código 404 le indica al navegador que el recurso no fue encontrado
    return "Producto no encontrado", 404

@app.route('/api/search')
def api_search():
    """
    API REST: Endpoint de búsqueda que devuelve JSON
    =================================================
    
    URL: http://localhost:5000/api/search
    Método HTTP: GET
    
    Parámetros de URL opcionales:
    - q: Término de búsqueda
      Ejemplo: /api/search?q=rolex
    - category: Categoría a filtrar ('all', 'watch', 'jewelry')
      Ejemplo: /api/search?category=watch
    - Ambos: /api/search?q=rolex&category=watch
    
    Diferencias con la ruta index():
    - Esta ruta devuelve JSON (para consumir desde JavaScript/AJAX o apps externas)
    - La ruta index() devuelve HTML (para mostrar en el navegador)
    
    Uso típico:
    - Búsquedas dinámicas sin recargar la página (AJAX)
    - Integración con aplicaciones móviles o de terceros
    - APIs públicas para desarrolladores externos
    
    Proceso:
    1. Lee los parámetros de búsqueda
    2. Filtra productos (igual que index())
    3. Convierte la lista a JSON y la devuelve
    
    Retorna:
    - JSON con la lista de productos que coinciden con la búsqueda
    
    Ejemplo de respuesta JSON:
    [
      {
        "id": 1,
        "name": "Rolex Submariner",
        "category": "watch",
        "price": 12500.00,
        "description": "...",
        "image": "..."
      }
    ]
    """
    # Paso 1: Obtener parámetros de la URL
    # Nota: se usa 'q' en lugar de 'search' (convención para APIs)
    query = request.args.get('q', '').lower()       # Término de búsqueda
    category = request.args.get('category', 'all')  # Categoría seleccionada
    
    # Paso 2: Comenzar con todos los productos
    filtered = products
    
    # Paso 3: Aplicar filtro de categoría
    if category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
    
    # Paso 4: Aplicar filtro de búsqueda
    if query:
        filtered = [p for p in filtered 
                   if query in p['name'].lower() or query in p['description'].lower()]
    
    # Paso 5: Convertir lista Python a JSON y devolverla
    # jsonify() convierte automáticamente estructuras Python a JSON
    # y establece el Content-Type correcto (application/json)
    return jsonify(filtered)

# ============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ============================================================================
# Este bloque solo se ejecuta cuando se corre el archivo directamente
# (no cuando se importa como módulo)
# ============================================================================
if __name__ == '__main__':
    """
    Configuración y ejecución del servidor Flask
    ============================================
    
    Parámetros de app.run():
    - debug=False: Modo producción (no muestra errores detallados al usuario)
                   En desarrollo, cambiar a True para ver errores completos
    - host='0.0.0.0': Acepta conexiones de cualquier IP
                      Esto permite acceder desde otras máquinas en la red
                      Para solo local, usar host='127.0.0.1'
    - port=5000: Puerto donde escucha el servidor
                 La aplicación estará disponible en http://localhost:5000
    
    Para ejecutar:
    $ python app.py
    
    Para detener:
    Presionar Ctrl+C en la terminal
    """
    # Iniciar el servidor web Flask
    app.run(debug=False, host='0.0.0.0', port=5000)
