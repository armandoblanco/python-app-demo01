# 🧪 Documentación de Pruebas - Python App Demo01

## 📋 Resumen de Resultados

**Estado de las Pruebas:** ✅ TODOS LOS TESTS PASARON

**Total de Tests:** 33
- ✅ Pasados: 33
- ❌ Fallidos: 0
- ⚠️ Omitidos: 0

**Cobertura de Código:** 97%
- Statements totales: 31
- Statements cubiertos: 30
- Statements sin cubrir: 1

**Tiempo de Ejecución:** 0.26s

---

## 📂 Estructura de Pruebas

### Clases de Test Implementadas

#### 1. **TestIndexRoute** (9 tests)
Prueba la ruta principal de la aplicación (`/`)
- ✅ test_index_loads_successfully
- ✅ test_index_displays_all_products
- ✅ test_index_filter_by_watch_category
- ✅ test_index_filter_by_jewelry_category
- ✅ test_index_search_functionality
- ✅ test_index_search_case_insensitive
- ✅ test_index_search_in_description
- ✅ test_index_search_no_results
- ✅ test_index_combined_filter_and_search

#### 2. **TestProductDetailRoute** (4 tests)
Prueba la ruta de detalle de productos (`/product/<id>`)
- ✅ test_product_detail_valid_id
- ✅ test_product_detail_another_valid_id
- ✅ test_product_detail_invalid_id
- ✅ test_product_detail_displays_price

#### 3. **TestAPISearch** (8 tests)
Prueba el endpoint de API de búsqueda (`/api/search`)
- ✅ test_api_search_returns_json
- ✅ test_api_search_all_products
- ✅ test_api_search_with_query
- ✅ test_api_search_by_category
- ✅ test_api_search_jewelry_category
- ✅ test_api_search_combined_query_and_category
- ✅ test_api_search_case_insensitive
- ✅ test_api_search_no_results

#### 4. **TestProductsData** (9 tests)
Prueba la estructura y validez de los datos de productos
- ✅ test_products_count
- ✅ test_products_have_required_fields
- ✅ test_product_ids_are_unique
- ✅ test_product_categories_are_valid
- ✅ test_product_prices_are_positive
- ✅ test_watches_count
- ✅ test_jewelry_count
- ✅ test_product_names_are_not_empty
- ✅ test_product_descriptions_are_not_empty

#### 5. **TestAppConfiguration** (3 tests)
Prueba la configuración de la aplicación Flask
- ✅ test_app_exists
- ✅ test_app_is_flask_instance
- ✅ test_testing_mode

---

## 🚀 Cómo Ejecutar las Pruebas

### Instalación de Dependencias

```bash
# Instalar dependencias principales
pip install -r requirements.txt

# Instalar dependencias de desarrollo y testing
pip install -r requirements-dev.txt
```

### Ejecutar Todas las Pruebas

```bash
# Ejecución básica
pytest test_app.py

# Ejecución con salida detallada
pytest test_app.py -v

# Ejecución con reporte de cobertura
pytest test_app.py --cov=app --cov-report=term

# Ejecución con reportes completos (HTML + Coverage)
pytest test_app.py -v --cov=app --cov-report=html --cov-report=term --html=test-report.html --self-contained-html
```

### Ejecutar Pruebas Específicas

```bash
# Ejecutar una clase específica de tests
pytest test_app.py::TestIndexRoute -v

# Ejecutar un test específico
pytest test_app.py::TestIndexRoute::test_index_loads_successfully -v
```

---

## 📊 Reportes Generados

### 1. Reporte de Cobertura HTML
- **Ubicación:** `htmlcov/index.html`
- **Descripción:** Reporte interactivo que muestra línea por línea qué código fue ejecutado durante las pruebas
- **Cómo ver:** Abrir `htmlcov/index.html` en un navegador web

### 2. Reporte de Tests HTML
- **Ubicación:** `test-report.html`
- **Descripción:** Reporte detallado con resultados de cada test, tiempos de ejecución y metadata del ambiente
- **Cómo ver:** Abrir `test-report.html` en un navegador web

### 3. Reporte de Cobertura Terminal
```
Name     Stmts   Miss  Cover
----------------------------
app.py      31      1    97%
----------------------------
TOTAL       31      1    97%
```

---

## 🎯 Áreas de Cobertura

### Funcionalidades Probadas

#### ✅ Rutas HTTP
- Página principal (`/`)
- Detalle de productos (`/product/<id>`)
- API de búsqueda (`/api/search`)

#### ✅ Filtrado y Búsqueda
- Filtrado por categoría (relojes/joyas)
- Búsqueda por nombre de producto
- Búsqueda por descripción
- Búsqueda case-insensitive
- Combinación de filtros y búsqueda

#### ✅ Validación de Datos
- Integridad de datos de productos
- Validación de campos requeridos
- Validación de tipos de datos
- Validación de IDs únicos

#### ✅ Manejo de Errores
- Productos no encontrados (404)
- Búsquedas sin resultados
- IDs inválidos

---

## 🔧 Tecnologías de Testing Utilizadas

- **pytest 7.4.3** - Framework de testing
- **pytest-cov 4.1.0** - Plugin para medir cobertura de código
- **pytest-html 4.1.1** - Plugin para generar reportes HTML
- **Flask Testing** - Utilidades de testing integradas en Flask

---

## 📈 Métricas de Calidad

| Métrica | Valor | Estado |
|---------|-------|--------|
| Tests Totales | 33 | ✅ |
| Tests Pasados | 33 (100%) | ✅ |
| Cobertura de Código | 97% | ✅ |
| Tiempo de Ejecución | 0.26s | ✅ Rápido |

---

## 🎓 Casos de Prueba Destacados

### Caso 1: Búsqueda Combinada
**Test:** `test_index_combined_filter_and_search`
**Descripción:** Verifica que se puede filtrar por categoría y buscar texto simultáneamente
**Entrada:** `/?category=watch&search=omega`
**Resultado Esperado:** Solo productos de tipo "watch" que contengan "omega"

### Caso 2: Validación de Datos
**Test:** `test_products_have_required_fields`
**Descripción:** Asegura que todos los productos tengan los campos necesarios
**Campos Validados:** id, name, category, price, description, image

### Caso 3: API JSON
**Test:** `test_api_search_returns_json`
**Descripción:** Verifica que el endpoint de API devuelva datos en formato JSON correcto
**Endpoint:** `/api/search`

---

## 🔄 Integración Continua

Estos tests están diseñados para ser ejecutados en pipelines de CI/CD. Se recomienda:

1. Ejecutar tests en cada push
2. Generar reportes de cobertura
3. Fallar el build si la cobertura cae por debajo del 90%
4. Archivar reportes HTML como artefactos

### Ejemplo de Configuración GitHub Actions

```yaml
- name: Run tests
  run: |
    pip install -r requirements-dev.txt
    pytest test_app.py -v --cov=app --cov-report=html --html=test-report.html --self-contained-html

- name: Upload test results
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: |
      htmlcov/
      test-report.html
```

---

## 📝 Notas Adicionales

- Los archivos de reporte (`htmlcov/`, `test-report.html`, `.coverage`) están excluidos del control de versiones via `.gitignore`
- Los tests son independientes y pueden ejecutarse en cualquier orden
- Todos los tests utilizan un cliente de prueba de Flask (`test_client`) para simular requests HTTP
- No se requiere una base de datos ya que los productos están en memoria

---

## 📞 Soporte

Si encuentras algún problema con las pruebas o tienes sugerencias para mejorarlas, por favor abre un issue en el repositorio.

---

**Fecha de Generación:** Diciembre 2024
**Versión de la Aplicación:** 1.0.0
**Autor:** Equipo de Desarrollo Python App Demo01
