# Documentación - Diagramas UML

Esta carpeta contiene la documentación técnica del sistema E-commerce de Relojes de Lujo y Joyas.

## Contenido

### diagrama_secuencia_uml.drawio

Diagrama de secuencia UML que muestra las interacciones entre los componentes del sistema:

- **Usuario**: Actor que interactúa con la aplicación
- **Frontend (HTML/CSS/JS)**: Interfaz de usuario (puerto 8000)
- **Backend API (Flask)**: API RESTful (puerto 5000)
- **Catálogo (Memoria)**: Almacenamiento en memoria de productos

#### Escenarios incluidos:

1. **Visualizar Catálogo**: 
   - Usuario accede a la página principal
   - Frontend solicita lista de productos al Backend
   - Backend consulta el catálogo y retorna JSON
   - Frontend renderiza los productos

2. **Filtrar por Categoría**:
   - Usuario selecciona categoría (Relojes/Joyas)
   - Frontend solicita productos filtrados
   - Backend filtra y retorna productos según categoría
   - Frontend actualiza la vista

3. **Ver Detalle de Producto**:
   - Usuario hace clic en un producto específico
   - Frontend solicita detalles del producto por ID
   - Backend busca y retorna datos del producto
   - Frontend muestra página de detalle

## Cómo abrir el diagrama

El archivo `.drawio` puede ser abierto con:

1. **Draw.io Desktop**: Descarga la aplicación desde https://github.com/jgraph/drawio-desktop/releases
2. **Draw.io Web**: Visita https://app.diagrams.net y abre el archivo
3. **VS Code**: Instala la extensión "Draw.io Integration" y abre el archivo directamente

## Formato del archivo

El archivo está en formato XML compatible con Draw.io/diagrams.net, que es el estándar de la industria para diagramas técnicos.

## Arquitectura del Sistema

Este diagrama complementa la documentación existente en:
- `ARCHITECTURE.md`: Arquitectura completa del sistema
- `COMPONENT_DIAGRAM.md`: Diagramas de componentes
- `MIGRATION_GUIDE.md`: Guía de migración

## Notas técnicas

- El diagrama utiliza notación UML estándar para diagramas de secuencia
- Las flechas sólidas (→) representan llamadas síncronas
- Las flechas punteadas (⇢) representan respuestas
- Los rectángulos verticales representan activación de componentes
- Las líneas verticales punteadas son líneas de vida de los objetos
