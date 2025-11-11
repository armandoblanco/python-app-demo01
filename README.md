# python-app-demo01
E-commerce de Relojes de Lujo y Joyas

## Descripción
Aplicación web de e-commerce para vender relojes de lujo y joyas, desarrollada con PHP y JavaScript. Presenta un catálogo elegante con 10 productos exclusivos, funcionalidad de búsqueda y filtrado por categoría.

## Características
- ✨ Catálogo con 10 productos (5 relojes de lujo y 5 joyas exclusivas)
- 🔍 Búsqueda dinámica de productos
- 📁 Filtrado por categoría (Relojes / Joyas)
- 💰 Precios en USD con formato profesional
- 📱 Diseño responsive y elegante (negro, dorado, blanco)
- 🖼️ Imágenes placeholder para cada producto
- 📄 Página de detalle para cada producto

## Tecnologías
- **Backend**: PHP 8.3+
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de datos**: Sin base de datos (productos en memoria con arrays PHP)

## Requisitos Previos

- PHP 8.0 o superior
- Navegador web moderno

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/armandoblanco/python-app-demo01.git
cd python-app-demo01
```

2. No se requieren dependencias adicionales. PHP viene con todo lo necesario.

## Ejecución

### Opción 1: Servidor PHP integrado (desarrollo)
```bash
php -S localhost:8000
```

La aplicación estará disponible en: `http://localhost:8000`

### Opción 2: Servidor web Apache/Nginx (producción)
Configurar el DocumentRoot apuntando al directorio del proyecto y acceder a través del navegador.

## Estructura del Proyecto
```
python-app-demo01/
├── index.php                   # Página principal con catálogo
├── product_detail.php          # Página de detalle del producto
├── api_search.php              # API de búsqueda JSON
├── products.php                # Datos de productos (catálogo)
└── templates/                  # Templates HTML originales (legacy)
    ├── index.html
    └── product_detail.html
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

### Detalles del Producto
- Imagen del producto
- Nombre y categoría
- Precio en USD
- Descripción detallada
- Características destacadas
- Botones de acción (demo)

## Endpoints Disponibles

- `GET /index.php` - Página principal con catálogo
  - Parámetros: `?category={all|watch|jewelry}&search={query}`
- `GET /product_detail.php?id={id}` - Detalle de producto específico
- `GET /api_search.php?q={query}&category={category}` - API de búsqueda JSON

## Ejemplos de Uso

### Búsqueda por categoría
```
http://localhost:8000/index.php?category=watch
```

### Búsqueda por texto
```
http://localhost:8000/index.php?search=rolex
```

### API de búsqueda
```bash
curl "http://localhost:8000/api_search.php?q=diamond&category=jewelry"
```

## Licencia
MIT License - Ver archivo [LICENSE](LICENSE) para más detalles
