# Guía de Migración y Actualización

## Resumen de Cambios

Este documento proporciona una guía paso a paso para migrar de la arquitectura monolítica a la arquitectura desacoplada, así como instrucciones para despliegue y actualización del sistema.

## Cambios Principales

### Estructura del Proyecto

**ANTES:**
```
python-app-demo01/
├── app.py                  # Aplicación monolítica
├── requirements.txt
└── templates/
    ├── index.html         # Templates con Flask
    └── product_detail.html
```

**DESPUÉS:**
```
python-app-demo01/
├── app.py                  # ⚠️ DEPRECATED - mantener para compatibilidad
├── backend/
│   └── api.py             # ✨ NUEVO - API RESTful
├── frontend/
│   ├── index.html         # ✨ NUEVO - Frontend independiente
│   ├── product.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── config.js
│       ├── api.js
│       ├── app.js
│       └── product.js
├── tests/
│   └── test_api.py        # ✨ NUEVO - Tests automatizados
├── templates/             # ⚠️ DEPRECATED
├── requirements.txt       # ✅ ACTUALIZADO
├── ARCHITECTURE.md        # ✨ NUEVO - Documentación
└── MIGRATION_GUIDE.md     # ✨ NUEVO - Esta guía
```

## Plan de Migración

### Fase 1: Preparación (Completada ✅)

#### 1.1 Instalación de Dependencias Nuevas

```bash
pip install -r requirements.txt
```

**Nuevas dependencias agregadas:**
- `flask-cors==4.0.0` - Para habilitar CORS en el backend
- `pytest==7.4.3` - Framework de testing
- `pytest-flask==1.3.0` - Testing para Flask

#### 1.2 Verificación de Compatibilidad

- ✅ Python 3.x requerido
- ✅ Flask 3.0.0 compatible
- ✅ Sin conflictos de dependencias

### Fase 2: Backend API (Completada ✅)

#### 2.1 Crear Backend API

El nuevo backend API está en `/backend/api.py` y proporciona:

- **Endpoints RESTful:**
  - `GET /api/health` - Health check
  - `GET /api/products` - Lista de productos con filtros
  - `GET /api/products/<id>` - Detalle de producto
  - `GET /api/categories` - Categorías disponibles

- **Características:**
  - CORS habilitado
  - Respuestas JSON estandarizadas
  - Manejo de errores
  - Validación de parámetros

#### 2.2 Testing del Backend

```bash
# Ejecutar tests
python -m pytest tests/test_api.py -v

# Resultado esperado: 13 tests passed
```

#### 2.3 Iniciar Backend

```bash
# Opción 1: Directamente
python backend/api.py

# Opción 2: Con Flask CLI
export FLASK_APP=backend/api.py
flask run --port 5000

# Verificar que está corriendo:
curl http://localhost:5000/api/health
```

### Fase 3: Frontend Desacoplado (Completada ✅)

#### 3.1 Estructura del Frontend

El frontend ahora es completamente independiente:

- **HTML:** Páginas sin dependencias de templates Flask
- **CSS:** Estilos unificados en `/frontend/css/styles.css`
- **JavaScript:** Lógica del cliente en `/frontend/js/`

#### 3.2 Configuración del Frontend

Editar `/frontend/js/config.js` para apuntar al backend:

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',  // Cambiar en producción
    // ...
};
```

#### 3.3 Servir Frontend

```bash
# Opción 1: Servidor Python simple (desarrollo)
cd frontend
python -m http.server 8000

# Opción 2: Con Node.js http-server (si está instalado)
cd frontend
npx http-server -p 8000

# Opción 3: Con nginx (producción)
# Ver sección de despliegue más abajo
```

#### 3.4 Verificar Frontend

Abrir navegador en: `http://localhost:8000`

### Fase 4: Testing y Validación

#### 4.1 Tests Automatizados

```bash
# Tests de backend
python -m pytest tests/test_api.py -v

# Coverage report (opcional)
python -m pytest tests/test_api.py --cov=backend --cov-report=html
```

#### 4.2 Validación Manual

1. **Backend API:**
   ```bash
   # Health check
   curl http://localhost:5000/api/health
   
   # Lista de productos
   curl http://localhost:5000/api/products
   
   # Producto específico
   curl http://localhost:5000/api/products/1
   
   # Filtrar por categoría
   curl http://localhost:5000/api/products?category=watch
   
   # Búsqueda
   curl http://localhost:5000/api/products?search=rolex
   ```

2. **Frontend:**
   - Abrir `http://localhost:8000`
   - Probar búsqueda
   - Probar filtros de categoría
   - Hacer clic en productos
   - Verificar página de detalle

#### 4.3 Checklist de Funcionalidad

- [ ] Backend API responde correctamente
- [ ] Frontend se carga sin errores
- [ ] Búsqueda funciona en tiempo real
- [ ] Filtros de categoría funcionan
- [ ] Navegación a detalle de producto funciona
- [ ] Botón "Volver" funciona
- [ ] Diseño responsive funciona en móvil
- [ ] No hay errores en la consola del navegador

## Despliegue a Producción

### Opción 1: Despliegue Tradicional

#### Backend (Flask)

```bash
# 1. Instalar en servidor
git clone <repository>
cd python-app-demo01
pip install -r requirements.txt

# 2. Usar servidor WSGI de producción
pip install gunicorn

# 3. Iniciar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.api:app

# O con uWSGI
pip install uwsgi
uwsgi --http :5000 --wsgi-file backend/api.py --callable app
```

#### Frontend (Archivos Estáticos)

```bash
# Opción 1: Nginx
# /etc/nginx/sites-available/frontend
server {
    listen 80;
    server_name yourdomain.com;
    
    root /path/to/python-app-demo01/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# Opción 2: Apache
# /etc/apache2/sites-available/frontend.conf
<VirtualHost *:80>
    ServerName yourdomain.com
    DocumentRoot /path/to/python-app-demo01/frontend
    
    <Directory /path/to/python-app-demo01/frontend>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

### Opción 2: Despliegue con Docker

#### Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.api:app"]
```

#### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM nginx:alpine

COPY frontend/ /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

**Comandos:**
```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Opción 3: Despliegue en Cloud

#### Heroku

**Backend:**
```bash
# Crear Procfile
echo "web: gunicorn backend.api:app" > Procfile

# Desplegar
heroku create myapp-backend
git push heroku main
```

**Frontend:**
```bash
# Usar servicio de hosting estático
# - Netlify
# - Vercel
# - GitHub Pages
# - AWS S3 + CloudFront
```

#### AWS (Arquitectura Recomendada)

```
┌─────────────────┐
│   CloudFront    │ ← CDN para frontend
└────────┬────────┘
         │
         ├──────────► S3 Bucket (Frontend estático)
         │
         └──────────► ALB ──► ECS/Lambda (Backend API)
```

## Configuración por Ambiente

### Desarrollo

```javascript
// frontend/js/config.js
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',
    // ...
};
```

### Producción

```javascript
// frontend/js/config.js
const CONFIG = {
    API_BASE_URL: 'https://api.yourdomain.com',
    // ...
};
```

**Alternativa:** Usar variables de entorno

```javascript
// frontend/js/config.js
const CONFIG = {
    API_BASE_URL: window.ENV?.API_URL || 'http://localhost:5000',
    // ...
};
```

```html
<!-- Inyectar en index.html -->
<script>
    window.ENV = {
        API_URL: '{{ API_URL }}'
    };
</script>
```

## Monitoreo y Mantenimiento

### Logs del Backend

```python
# backend/api.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Health Checks

```bash
# Monitorear el health endpoint
watch -n 5 'curl -s http://localhost:5000/api/health'

# O con un script de monitoreo
# monitors/health_check.sh
#!/bin/bash
while true; do
    STATUS=$(curl -s http://localhost:5000/api/health | jq -r .status)
    if [ "$STATUS" != "healthy" ]; then
        echo "ALERT: Backend unhealthy!"
        # Enviar notificación
    fi
    sleep 60
done
```

## Rollback Plan

Si es necesario volver a la versión anterior:

### Opción 1: Usar app.py original

```bash
# Detener servicios nuevos
# Iniciar app original
python app.py
```

### Opción 2: Git revert

```bash
# Revertir commit
git revert <commit-hash>
git push

# O regresar a tag anterior
git checkout <previous-tag>
```

## Problemas Comunes y Soluciones

### 1. Error de CORS

**Problema:** Frontend no puede conectar con backend
```
Access to fetch at 'http://localhost:5000/api/products' from origin 
'http://localhost:8000' has been blocked by CORS policy
```

**Solución:**
- Verificar que flask-cors está instalado
- Verificar que CORS(app) está en backend/api.py
- En producción, configurar origins específicos:

```python
CORS(app, origins=['https://yourdomain.com'])
```

### 2. Puerto en Uso

**Problema:** `Address already in use`

**Solución:**
```bash
# Encontrar proceso usando el puerto
lsof -i :5000
# O en Linux
netstat -tulpn | grep :5000

# Matar proceso
kill -9 <PID>
```

### 3. Módulo no Encontrado

**Problema:** `ModuleNotFoundError: No module named 'flask_cors'`

**Solución:**
```bash
pip install -r requirements.txt
# O específicamente
pip install flask-cors
```

### 4. Frontend no Carga Datos

**Problema:** Frontend muestra "Cargando..." indefinidamente

**Solución:**
1. Verificar que backend está corriendo: `curl http://localhost:5000/api/health`
2. Revisar consola del navegador (F12)
3. Verificar URL en config.js
4. Verificar CORS

## Siguientes Pasos

1. ✅ **Migración Completada**
   - Backend API funcionando
   - Frontend desacoplado
   - Tests pasando

2. 🔄 **Despliegue a Staging**
   - Configurar ambiente de staging
   - Desplegar y probar
   - Validar con usuarios de prueba

3. 🚀 **Despliegue a Producción**
   - Configurar infraestructura
   - Migrar DNS si es necesario
   - Monitoreo activo

4. 📊 **Post-Deployment**
   - Monitorear logs
   - Analizar performance
   - Recopilar feedback

## Soporte

Para problemas o preguntas:
1. Revisar esta guía y ARCHITECTURE.md
2. Revisar logs de backend y consola del navegador
3. Verificar configuración de red/CORS
4. Contactar al equipo de desarrollo

## Changelog

### v2.0.0 (Actual)
- ✨ Arquitectura desacoplada
- ✨ Backend API RESTful
- ✨ Frontend independiente
- ✨ Tests automatizados
- ✨ Documentación completa

### v1.0.0 (Anterior)
- Aplicación monolítica con Flask
- Templates Jinja2
- Sin tests automatizados
