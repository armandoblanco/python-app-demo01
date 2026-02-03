# python-app-demo01
E-commerce de Relojes de Lujo y Joyas

## Descripción
Aplicación web de e-commerce para vender relojes de lujo y joyas, desarrollada con Python y Flask. Presenta un catálogo elegante con 10 productos exclusivos, funcionalidad de búsqueda y filtrado por categoría.

## Características
- ✨ Catálogo con 10 productos (5 relojes de lujo y 5 joyas exclusivas)
- 🔍 Búsqueda dinámica de productos
- 📁 Filtrado por categoría (Relojes / Joyas)
- 🛒 Carrito de compras con gestión de cantidades
- 💰 Precios en USD con formato profesional
- 🧮 Cálculo automático de impuestos (IVA 19%)
- 📄 Generación de facturas en PDF
- 📱 Diseño responsive y elegante (negro, dorado, blanco)
- 🖼️ Imágenes placeholder para cada producto
- 📄 Página de detalle para cada producto

## Tecnologías
- **Backend**: Flask 3.0.0
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Generation**: ReportLab 4.0.7
- **Base de datos**: Sin base de datos (productos en memoria con diccionarios)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/armandoblanco/python-app-demo01.git
cd python-app-demo01
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Ejecutar la aplicación:
```bash
python app.py
```

Para producción, configure la variable de entorno SECRET_KEY:
```bash
export SECRET_KEY=your-secure-random-key
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Estructura del Proyecto
```
python-app-demo01/
├── app.py                      # Aplicación Flask principal
├── requirements.txt            # Dependencias Python
├── templates/
│   ├── index.html             # Página principal con catálogo
│   └── product_detail.html    # Página de detalle del producto
└── static/
    ├── css/
    └── js/
```

## Productos Disponibles

### Relojes de Lujo
1. Rolex Submariner - $12,500.00
2. Patek Philippe Nautilus - $35,000.00
3. Audemars Piguet Royal Oak - $28,000.00
4. Omega Speedmaster - $6,500.00
5. Cartier Santos - $7,200.00

### Joyas Exclusivas
6. Collar de Diamantes - $15,000.00
7. Anillo de Compromiso - $8,500.00
8. Brazalete de Oro - $4,200.00
9. Pendientes de Esmeralda - $9,800.00
10. Broche de Zafiro - $6,700.00

## Funcionalidades Principales

### Búsqueda
- Búsqueda en tiempo real por nombre o descripción
- Búsqueda combinada con filtros de categoría

### Filtros
- Todos los productos
- Solo relojes de lujo
- Solo joyas exclusivas

### Carrito de Compras
- Agregar productos al carrito
- Actualizar cantidades
- Eliminar productos del carrito
- Cálculo automático de subtotal, impuestos y total
- Tasa de impuesto del 19% (IVA Chile)

### Facturación
- Generación automática de facturas en PDF
- Incluye número de factura único
- Fecha y hora de emisión
- Detalle de productos con cantidades y precios
- Cálculo de impuestos
- Total a pagar

### Detalles del Producto
- Imagen del producto
- Nombre y categoría
- Precio en USD
- Descripción detallada
- Características destacadas
- Botón para agregar al carrito

## API Endpoints

- `GET /` - Página principal con catálogo
- `GET /product/<id>` - Detalle de producto específico
- `GET /cart` - Página del carrito de compras
- `GET /api/search?q=<query>&category=<category>` - API de búsqueda JSON
- `GET /api/cart` - Obtener contenido actual del carrito
- `POST /api/cart/add` - Agregar producto al carrito
- `POST /api/cart/update` - Actualizar cantidad de producto en carrito
- `POST /api/cart/remove` - Eliminar producto del carrito
- `POST /api/invoice/generate` - Generar y descargar factura PDF

## Licencia
MIT License - Ver archivo [LICENSE](LICENSE) para más detalles
