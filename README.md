# python-app-demo01
E-commerce de Relojes de Lujo y Joyas - **Arquitectura Desacoplada**

## Descripción
Aplicación web de e-commerce para vender relojes de lujo y joyas, desarrollada con arquitectura desacoplada: Frontend independiente y Backend API RESTful. Presenta un catálogo elegante con 10 productos exclusivos, funcionalidad de búsqueda y filtrado por categoría.

## 🆕 Nueva Arquitectura (v2.0)

La aplicación ha sido **rediseñada completamente** con arquitectura desacoplada:
- ✅ **Frontend independiente** (HTML/CSS/JS) - Puerto 8000
- ✅ **Backend API RESTful** (Flask) - Puerto 5000
- ✅ **Comunicación via API** con CORS habilitado
- ✅ **Tests automatizados** con pytest
- ✅ **Documentación completa** de arquitectura

### Ventajas de la Nueva Arquitectura
- 🚀 Desarrollo independiente de frontend y backend
- 📦 Despliegue separado y escalable
- 🧪 Tests automatizados
- 🔄 Flexibilidad para múltiples clientes (web, mobile, etc.)
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
- **Backend**: Flask 3.0.0 + Flask-CORS 4.0.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Testing**: pytest 7.4.3, pytest-flask 1.3.0
- **Base de datos**: En memoria (productos en array)

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

### Opción 1: Ejecutar Ambos Servicios (Desarrollo)

**Terminal 1 - Backend API:**
```bash
python backend/api.py
```
Backend disponible en: `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 8000
```
Frontend disponible en: `http://localhost:8000`

### Opción 2: Aplicación Original (Monolítica - Deprecated)
```bash
python app.py
```
Disponible en: `http://localhost:5000`

## Testing

Ejecutar tests automatizados:
```bash
# Todos los tests
python -m pytest tests/test_api.py -v

# Con coverage
python -m pytest tests/test_api.py --cov=backend --cov-report=html
```

## Estructura del Proyecto
```
python-app-demo01/
├── backend/
│   └── api.py                 # ✨ API RESTful Backend
├── frontend/
│   ├── index.html             # ✨ Catálogo (SPA)
│   ├── product.html           # ✨ Detalle de producto
│   ├── css/
│   │   └── styles.css         # Estilos unificados
│   └── js/
│       ├── config.js          # Configuración
│       ├── api.js             # Cliente API
│       ├── app.js             # Lógica del catálogo
│       └── product.js         # Lógica del detalle
├── tests/
│   └── test_api.py            # ✨ Tests automatizados
├── app.py                     # ⚠️ DEPRECATED (v1.0 monolítica)
├── templates/                 # ⚠️ DEPRECATED
├── requirements.txt           # Dependencias Python
├── ARCHITECTURE.md            # 📚 Documentación de arquitectura
├── MIGRATION_GUIDE.md         # 📚 Guía de migración
├── COMPONENT_DIAGRAM.md       # 📚 Diagrama de componentes
└── README.md                  # Este archivo
```

## API Endpoints

### Backend API (Puerto 5000)

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| GET | `/api/health` | Health check del servidor | - |
| GET | `/api/products` | Lista todos los productos | `?category=all\|watch\|jewelry`<br>`?search=término` |
| GET | `/api/products/<id>` | Detalle de un producto | - |
| GET | `/api/categories` | Lista de categorías disponibles | - |

### Ejemplos de Uso

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
- ✅ CORS habilitado para desarrollo cross-origin
- ✅ Filtrado y búsqueda en servidor
- ✅ Validación de parámetros
- ✅ Manejo de errores 404/500
- ✅ Health check endpoint

## Documentación Adicional

- 📚 **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura completa del sistema
- 📚 **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Guía de migración y despliegue
- 📚 **[COMPONENT_DIAGRAM.md](COMPONENT_DIAGRAM.md)** - Diagramas de componentes

## Licencia
MIT License - Ver archivo [LICENSE](LICENSE) para más detalles

## Changelog

### v2.0.0 (Actual) - Arquitectura Desacoplada
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
