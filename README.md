# python-app-demo01
E-commerce de Relojes de Lujo y Joyas - **Arquitectura Desacoplada**

## Descripción
Aplicación web de e-commerce para vender relojes de lujo y joyas, desarrollada con arquitectura desacoplada: Frontend independiente y Backend API RESTful. Presenta un catálogo elegante con 10 productos exclusivos, funcionalidad de búsqueda y filtrado por categoría.

## 🆕 Nueva Arquitectura (v3.0) - **Backends Duales**

La aplicación ha sido **rediseñada completamente** con arquitectura desacoplada y **ahora soporta dos backends**:
- ✅ **Frontend independiente** (HTML/CSS/JS) - Puerto 8000
- ✅ **Backend API RESTful Python** (Flask) - Puerto 5000
- ✅ **Backend API RESTful PHP** (Nativo) - Puerto 8080 ⭐ NUEVO
- ✅ **Comunicación via API** con CORS habilitado
- ✅ **Tests automatizados** con pytest y PHPUnit
- ✅ **Documentación completa** de arquitectura

### Ventajas de la Nueva Arquitectura
- 🚀 Desarrollo independiente de frontend y backend
- 📦 Despliegue separado y escalable
- 🧪 Tests automatizados (Python y PHP)
- 🔄 Flexibilidad para múltiples clientes (web, mobile, etc.)
- 🎯 **Dual backend support** - Elige Python o PHP
- 📚 Documentación detallada

## Características
- ✨ Catálogo con 10 productos (5 relojes de lujo y 5 joyas exclusivas)
- 🔍 Búsqueda dinámica de productos con debouncing
- 📁 Filtrado por categoría (Relojes / Joyas)
- 💰 Precios en USD con formato profesional
- 📱 Diseño responsive y elegante (negro, dorado, blanco)
- 🖼️ Imágenes placeholder para cada producto
- 📄 Página de detalle para cada producto
- 🔌 API RESTful completa
- ✅ 13 tests automatizados

## Tecnologías
- **Backend Python**: Flask 3.0.0 + Flask-CORS 4.0.0
- **Backend PHP**: PHP 7.4+ (Nativo) ⭐ NUEVO
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Testing Python**: pytest 7.4.3, pytest-flask 1.3.0
- **Testing PHP**: PHPUnit 10.0 ⭐ NUEVO
- **Base de datos**: En memoria (productos en array)

## Instalación

### Backend Python

1. Clonar el repositorio:
```bash
git clone https://github.com/armandoblanco/python-app-demo01.git
cd python-app-demo01
```

2. Instalar dependencias Python:
```bash
pip install -r requirements.txt
```

### Backend PHP

1. Instalar dependencias PHP (para tests):
```bash
cd backend-php
composer install
```

## Ejecución

### Opción 1: Backend Python + Frontend

**Terminal 1 - Backend API Python:**
```bash
python backend/api.py
```
Backend disponible en: `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
# Editar frontend/js/config.js: BACKEND_TYPE: 'python'
python -m http.server 8000
```
Frontend disponible en: `http://localhost:8000`

### Opción 2: Backend PHP + Frontend ⭐ NUEVO

**Terminal 1 - Backend API PHP:**
```bash
cd backend-php
php -S localhost:8080
```
Backend disponible en: `http://localhost:8080`

**Terminal 2 - Frontend:**
```bash
cd frontend
# Editar frontend/js/config.js: BACKEND_TYPE: 'php'
python -m http.server 8000
```
Frontend disponible en: `http://localhost:8000`

### Opción 3: Aplicación Original (Monolítica - Deprecated)
```bash
python app.py
```
Disponible en: `http://localhost:5000`

## Testing

### Tests Python (Backend Flask)
```bash
# Todos los tests
python -m pytest tests/test_api.py -v

# Con coverage
python -m pytest tests/test_api.py --cov=backend --cov-report=html
```

### Tests PHP (Backend PHP) ⭐ NUEVO
```bash
cd backend-php

# Instalar dependencias
composer install

# Ejecutar tests
./vendor/bin/phpunit

# Tests con verbose
./vendor/bin/phpunit --verbose
```

## Estructura del Proyecto
```
python-app-demo01/
├── backend/
│   └── api.py                 # ✨ API RESTful Python Backend
├── backend-php/               # ⭐ NUEVO - API RESTful PHP Backend
│   ├── api/
│   │   ├── health.php        # Health check endpoint
│   │   ├── products.php      # Products list endpoint
│   │   ├── product.php       # Single product endpoint
│   │   └── categories.php    # Categories endpoint
│   ├── tests/
│   │   └── ApiTest.php       # PHPUnit tests
│   ├── products.php          # Product data
│   ├── index.php            # Router principal
│   ├── composer.json        # PHP dependencies
│   └── README.md            # PHP backend documentation
├── frontend/
│   ├── index.html             # ✨ Catálogo (SPA)
│   ├── product.html           # ✨ Detalle de producto
│   ├── css/
│   │   └── styles.css         # Estilos unificados
│   └── js/
│       ├── config.js          # ⭐ Configuración (soporta Python y PHP)
│       ├── api.js             # Cliente API
│       ├── app.js             # Lógica del catálogo
│       └── product.js         # Lógica del detalle
├── tests/
│   └── test_api.py            # ✨ Tests automatizados Python
├── app.py                     # ⚠️ DEPRECATED (v1.0 monolítica)
├── templates/                 # ⚠️ DEPRECATED
├── requirements.txt           # Dependencias Python
├── ARCHITECTURE.md            # 📚 Documentación de arquitectura
├── MIGRATION_GUIDE.md         # 📚 Guía de migración
├── PHP_MIGRATION.md           # ⭐ 📚 Guía de migración a PHP
├── COMPONENT_DIAGRAM.md       # 📚 Diagrama de componentes
└── README.md                  # Este archivo
```

## API Endpoints

### Backend Python API (Puerto 5000)

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| GET | `/api/health` | Health check del servidor | - |
| GET | `/api/products` | Lista todos los productos | `?category=all\|watch\|jewelry`<br>`?search=término` |
| GET | `/api/products/<id>` | Detalle de un producto | - |
| GET | `/api/categories` | Lista de categorías disponibles | - |

### Backend PHP API (Puerto 8080) ⭐ NUEVO

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| GET | `/api/health.php` | Health check del servidor | - |
| GET | `/api/products.php` | Lista todos los productos | `?category=all\|watch\|jewelry`<br>`?search=término` |
| GET | `/api/product.php?id={id}` | Detalle de un producto | `?id=1` |
| GET | `/api/categories.php` | Lista de categorías disponibles | - |

### Ejemplos de Uso

**Backend Python:**
```bash
# Health check
curl http://localhost:5000/api/health

# Todos los productos
curl http://localhost:5000/api/products

# Filtrar por categoría
curl http://localhost:5000/api/products?category=watch

# Buscar productos
curl http://localhost:5000/api/products?search=rolex

# Producto específico
curl http://localhost:5000/api/products/1
```

**Backend PHP:**
```bash
# Health check
curl http://localhost:8080/api/health.php

# Todos los productos
curl http://localhost:8080/api/products.php

# Filtrar por categoría
curl http://localhost:8080/api/products.php?category=watch

# Buscar productos
curl http://localhost:5000/api/products?search=rolex

# Producto específico
curl http://localhost:5000/api/products/1
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

### Frontend (SPA)
- ✅ Búsqueda en tiempo real con debouncing (500ms)
- ✅ Filtrado por categoría dinámico
- ✅ Navegación entre catálogo y detalle
- ✅ Diseño responsive (móvil, tablet, desktop)
- ✅ Animaciones y transiciones suaves
- ✅ Manejo de errores y estados de carga

### Backend (API)
- ✅ RESTful API con respuestas JSON estandarizadas
- ✅ **Dual Backend Support** - Python/Flask y PHP ⭐
- ✅ CORS habilitado para desarrollo cross-origin
- ✅ Filtrado y búsqueda en servidor
- ✅ Validación de parámetros
- ✅ Manejo de errores 404/500
- ✅ Health check endpoint

## Documentación Adicional

- 📚 **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura completa del sistema
- 📚 **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Guía de migración y despliegue
- 📚 **[PHP_MIGRATION.md](PHP_MIGRATION.md)** - Guía de migración a PHP ⭐ NUEVO
- 📚 **[backend-php/README.md](backend-php/README.md)** - Documentación del backend PHP
- 📚 **[COMPONENT_DIAGRAM.md](COMPONENT_DIAGRAM.md)** - Diagramas de componentes

## Licencia
MIT License - Ver archivo [LICENSE](LICENSE) para más detalles

## Changelog

### v3.0.0 (Actual) - Dual Backend Support ⭐
- ✨ **Backend PHP** implementado completamente
- ✨ Frontend soporta Python y PHP backends
- ✨ Tests PHP con PHPUnit (13 tests)
- ✨ Documentación completa de migración PHP
- ✨ Configuración flexible para cambiar backends
- ✅ 100% de funcionalidad preservada

### v2.0.0 - Arquitectura Desacoplada
- ✨ Nueva arquitectura frontend-backend separada
- ✨ API RESTful completa
- ✨ Frontend SPA independiente
- ✨ Tests automatizados (13 tests)
- ✨ Documentación completa de arquitectura
- ✨ CORS habilitado
- ✨ Búsqueda con debouncing

### v1.0.0 (Anterior) - Monolítica
- Aplicación monolítica con Flask y Templates
- Sin tests automatizados
- Frontend y backend acoplados
