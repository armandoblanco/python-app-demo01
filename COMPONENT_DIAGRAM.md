# Diagrama de Componentes del Sistema

## Vista General de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          SISTEMA E-COMMERCE                             │
│                  Relojes de Lujo y Joyas Santiago de Chile              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
         ┌──────────▼──────────┐         ┌─────────▼─────────┐
         │   FRONTEND (SPA)    │         │   BACKEND (API)   │
         │   Puerto: 8000      │◄───────►│   Puerto: 5000    │
         │   Servidor HTTP     │  HTTP   │   Flask + CORS    │
         └─────────────────────┘  JSON   └───────────────────┘
```

## Arquitectura de 3 Capas

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAPA DE PRESENTACIÓN                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐           │
│  │  index.html    │  │ product.html   │  │  styles.css    │           │
│  │                │  │                │  │                │           │
│  │  Catálogo de   │  │  Detalle del   │  │  Estilos       │           │
│  │  productos     │  │  producto      │  │  responsive    │           │
│  └────────┬───────┘  └────────┬───────┘  └────────────────┘           │
│           │                   │                                        │
│           └──────────┬────────┘                                        │
│                      │                                                 │
└──────────────────────┼─────────────────────────────────────────────────┘
                       │
┌──────────────────────┼─────────────────────────────────────────────────┐
│                      │       CAPA DE LÓGICA DE NEGOCIO                 │
├──────────────────────┼─────────────────────────────────────────────────┤
│                      │                                                 │
│  ┌───────────────────▼──────────┐  ┌──────────────────┐               │
│  │       app.js / product.js    │  │    api.js        │               │
│  │                              │  │                  │               │
│  │  • Renderizado dinámico      │──►  • HTTP Client  │               │
│  │  • Gestión de eventos        │  │  • Fetch API   │               │
│  │  • Filtrado y búsqueda       │  │  • Error       │               │
│  │  • State management          │  │    handling    │               │
│  └──────────────────────────────┘  └────────┬─────────┘               │
│                                              │                         │
└──────────────────────────────────────────────┼─────────────────────────┘
                                               │
                                               │ HTTP/JSON
                                               │
┌──────────────────────────────────────────────┼─────────────────────────┐
│                                              │  CAPA DE DATOS          │
├──────────────────────────────────────────────┼─────────────────────────┤
│                                              │                         │
│  ┌───────────────────────────────────────────▼──────────┐              │
│  │              Backend API (api.py)                    │              │
│  │                                                      │              │
│  │  ┌─────────────────┐  ┌────────────────────────┐   │              │
│  │  │  Flask Routes   │  │  Business Logic        │   │              │
│  │  │                 │  │                        │   │              │
│  │  │  /api/health    │  │  • Filtrado           │   │              │
│  │  │  /api/products  │──►  • Búsqueda           │   │              │
│  │  │  /api/products/<id>  • Validación          │   │              │
│  │  │  /api/categories│  │  • Transformación     │   │              │
│  │  └─────────────────┘  └───────────┬────────────┘   │              │
│  │                                   │                │              │
│  │                         ┌─────────▼──────────┐     │              │
│  │                         │  Data Store        │     │              │
│  │                         │  (In-Memory Array) │     │              │
│  │                         │  products[]        │     │              │
│  │                         └────────────────────┘     │              │
│  └────────────────────────────────────────────────────┘              │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## Componentes Detallados

### 1. Frontend Layer

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND COMPONENTS                       │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  HTML Pages                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐              ┌─────────────────┐      │
│  │  index.html     │              │ product.html    │      │
│  ├─────────────────┤              ├─────────────────┤      │
│  │ - Header        │              │ - Header        │      │
│  │ - Search Box    │              │ - Back Button   │      │
│  │ - Category      │              │ - Product       │      │
│  │   Filters       │              │   Details       │      │
│  │ - Product Grid  │              │ - Features      │      │
│  │ - Footer        │              │ - Action Buttons│      │
│  └─────────────────┘              └─────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  JavaScript Modules                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────┐  │
│  │  config.js   │    │   api.js     │    │   app.js    │  │
│  ├──────────────┤    ├──────────────┤    ├─────────────┤  │
│  │ • API URL    │───►│ APIClient    │◄───│ init()      │  │
│  │ • Endpoints  │    │ • request()  │    │ • load      │  │
│  │ • Timeouts   │    │ • get        │    │   Products()│  │
│  │ • Debounce   │    │   Products() │    │ • load      │  │
│  │   delay      │    │ • get        │    │   Categories│  │
│  └──────────────┘    │   Product()  │    │ • search    │  │
│                      │ • get        │    │ • filter    │  │
│                      │   Categories │    └─────────────┘  │
│                      └──────────────┘                     │
│                                                            │
│  ┌──────────────┐                                         │
│  │ product.js   │                                         │
│  ├──────────────┤                                         │
│  │ • init()     │                                         │
│  │ • load       │                                         │
│  │   Product    │                                         │
│  │   Detail()   │                                         │
│  │ • render     │                                         │
│  │   Features() │                                         │
│  └──────────────┘                                         │
│                                                            │
└────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Styles                                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────┐              │
│  │  styles.css                              │              │
│  ├──────────────────────────────────────────┤              │
│  │ • Base Styles                            │              │
│  │ • Header & Footer                        │              │
│  │ • Product Grid & Cards                   │              │
│  │ • Search & Filter Components             │              │
│  │ • Product Detail Layout                  │              │
│  │ • Responsive Design (@media queries)     │              │
│  │ • Animations & Transitions               │              │
│  └──────────────────────────────────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Backend Layer

```
┌──────────────────────────────────────────────────────────────┐
│                    BACKEND COMPONENTS                        │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Flask Application (api.py)                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  Flask App Configuration                   │            │
│  ├────────────────────────────────────────────┤            │
│  │  app = Flask(__name__)                     │            │
│  │  CORS(app)  # Enable cross-origin requests │            │
│  └────────────────────────────────────────────┘            │
│                                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  Data Layer                                │            │
│  ├────────────────────────────────────────────┤            │
│  │  products = [                              │            │
│  │    { id, name, category, price,            │            │
│  │      description, image },                 │            │
│  │    ...                                     │            │
│  │  ]                                         │            │
│  └────────────────────────────────────────────┘            │
│                                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  Route Handlers                            │            │
│  ├────────────────────────────────────────────┤            │
│  │                                            │            │
│  │  @app.route('/api/health')                 │            │
│  │  ┌──────────────────────────┐              │            │
│  │  │ health_check()           │              │            │
│  │  │ - Returns server status  │              │            │
│  │  └──────────────────────────┘              │            │
│  │                                            │            │
│  │  @app.route('/api/products')               │            │
│  │  ┌──────────────────────────┐              │            │
│  │  │ get_products()           │              │            │
│  │  │ - Parse query params     │              │            │
│  │  │ - Filter by category     │              │            │
│  │  │ - Search in name/desc    │              │            │
│  │  │ - Return JSON response   │              │            │
│  │  └──────────────────────────┘              │            │
│  │                                            │            │
│  │  @app.route('/api/products/<id>')          │            │
│  │  ┌──────────────────────────┐              │            │
│  │  │ get_product(id)          │              │            │
│  │  │ - Find product by ID     │              │            │
│  │  │ - Return JSON or 404     │              │            │
│  │  └──────────────────────────┘              │            │
│  │                                            │            │
│  │  @app.route('/api/categories')             │            │
│  │  ┌──────────────────────────┐              │            │
│  │  │ get_categories()         │              │            │
│  │  │ - Return category list   │              │            │
│  │  └──────────────────────────┘              │            │
│  │                                            │            │
│  └────────────────────────────────────────────┘            │
│                                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  Error Handlers                            │            │
│  ├────────────────────────────────────────────┤            │
│  │  @app.errorhandler(404)                    │            │
│  │  @app.errorhandler(500)                    │            │
│  └────────────────────────────────────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. Testing Layer

```
┌─────────────────────────────────────────────────────────────┐
│                    TESTING COMPONENTS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────┐              │
│  │  test_api.py                             │              │
│  ├──────────────────────────────────────────┤              │
│  │                                          │              │
│  │  ✓ test_health_check()                   │              │
│  │  ✓ test_get_all_products()               │              │
│  │  ✓ test_get_products_by_category()       │              │
│  │  ✓ test_search_products()                │              │
│  │  ✓ test_get_product_by_id()              │              │
│  │  ✓ test_get_product_not_found()          │              │
│  │  ✓ test_get_categories()                 │              │
│  │  ✓ test_404_endpoint()                   │              │
│  │  ✓ test_products_validation()            │              │
│  │                                          │              │
│  │  Total: 13 tests                         │              │
│  │  Coverage: Backend API routes            │              │
│  │                                          │              │
│  └──────────────────────────────────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Flujo de Comunicación

### Flujo 1: Carga Inicial de la Página

```
Usuario         Browser         Frontend JS      Backend API      Data Store
  │                │                │                │                │
  │  Visita URL    │                │                │                │
  ├───────────────►│                │                │                │
  │                │  Load HTML     │                │                │
  │                ├───────────────►│                │                │
  │                │                │  Health Check  │                │
  │                │                ├───────────────►│                │
  │                │                │◄───────────────┤                │
  │                │                │  GET           │                │
  │                │                │  /categories   │                │
  │                │                ├───────────────►│                │
  │                │                │◄───────────────┤                │
  │                │                │  GET           │  Query         │
  │                │                │  /products     │  products[]    │
  │                │                ├───────────────►├───────────────►│
  │                │                │                │◄───────────────┤
  │                │                │◄───────────────┤                │
  │                │  Render Page   │                │                │
  │                │◄───────────────┤                │                │
  │  Display       │                │                │                │
  │◄───────────────┤                │                │                │
  │                │                │                │                │
```

### Flujo 2: Búsqueda de Productos

```
Usuario         Browser         Frontend JS      Backend API      Data Store
  │                │                │                │                │
  │  Type Search   │                │                │                │
  ├───────────────►│  Input Event   │                │                │
  │                ├───────────────►│                │                │
  │                │                │  Debounce      │                │
  │                │                │  (500ms wait)  │                │
  │                │                │                │                │
  │                │                │  GET           │                │
  │                │                │  /products?    │  Filter        │
  │                │                │  search=query  │  products[]    │
  │                │                ├───────────────►├───────────────►│
  │                │                │                │◄───────────────┤
  │                │                │◄───────────────┤                │
  │                │  Update Grid   │                │                │
  │                │◄───────────────┤                │                │
  │  See Results   │                │                │                │
  │◄───────────────┤                │                │                │
  │                │                │                │                │
```

### Flujo 3: Ver Detalle de Producto

```
Usuario         Browser         Frontend JS      Backend API      Data Store
  │                │                │                │                │
  │  Click Product │                │                │                │
  ├───────────────►│  Navigate      │                │                │
  │                │  product.html? │                │                │
  │                │  id=1          │                │                │
  │                ├───────────────►│                │                │
  │                │                │  GET           │  Find          │
  │                │                │  /products/1   │  product by ID │
  │                │                ├───────────────►├───────────────►│
  │                │                │                │◄───────────────┤
  │                │                │◄───────────────┤                │
  │                │  Render Detail │                │                │
  │                │◄───────────────┤                │                │
  │  View Product  │                │                │                │
  │◄───────────────┤                │                │                │
  │                │                │                │                │
```

## Matriz de Responsabilidades

| Componente | Responsabilidades | Interactúa Con |
|-----------|-------------------|----------------|
| **index.html** | Estructura del catálogo | styles.css, app.js |
| **product.html** | Estructura del detalle | styles.css, product.js |
| **styles.css** | Presentación visual | Todos los HTML |
| **config.js** | Configuración centralizada | api.js, app.js, product.js |
| **api.js** | Comunicación HTTP | Backend API |
| **app.js** | Lógica del catálogo | api.js, DOM |
| **product.js** | Lógica del detalle | api.js, DOM |
| **api.py** | API RESTful | Ninguno (es el servidor) |
| **test_api.py** | Testing automatizado | api.py |

## Patrones de Diseño Utilizados

### 1. **MVC (Model-View-Controller)**
- **Model**: Data store (products array)
- **View**: HTML templates + CSS
- **Controller**: JavaScript modules + Flask routes

### 2. **API Gateway Pattern**
- Backend expone una API única
- Frontend consume API de forma consistente

### 3. **Single Responsibility Principle**
- Cada módulo tiene una responsabilidad clara
- Separación de presentación, lógica y datos

### 4. **Module Pattern**
- JavaScript organizado en módulos
- Encapsulación de funcionalidad

### 5. **Debouncing Pattern**
- Búsqueda optimizada con debounce
- Reduce llamadas innecesarias al backend

## Escalabilidad Futura

### Componentes que se Pueden Agregar:

```
┌─────────────────────────────────────────────────────────────┐
│  FUTURAS EXTENSIONES                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐      │
│  │  Database    │  │  Auth Service│  │  Payment    │      │
│  │  (PostgreSQL)│  │  (JWT/OAuth) │  │  Gateway    │      │
│  └──────────────┘  └──────────────┘  └─────────────┘      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐      │
│  │  Cache       │  │  Admin Panel │  │  Mobile App │      │
│  │  (Redis)     │  │  (React)     │  │  (React N.) │      │
│  └──────────────┘  └──────────────┘  └─────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Conclusión

Este diagrama muestra la arquitectura desacoplada del sistema, con clara separación de responsabilidades entre frontend y backend, facilitando el mantenimiento, testing y escalabilidad futura.
