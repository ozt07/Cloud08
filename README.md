API REST para Gestión de Estudiantes y Cursos

📋 Descripción
API REST desarrollada con Flask para gestionar estudiantes, cursos e inscripciones. Conexión con base de datos PostgreSQL en Supabase. Proyecto para Computación en la Nube - Actividad 8.

🚀 Tecnologías Utilizadas
- **Backend**: Flask (Python)
- **Base de Datos**: PostgreSQL (Supabase)
- **Despliegue**: Render
- **Autenticación**: API Key
- **CORS**: Flask-CORS

🔗 URL de la API en Producción
https://api-estudiantes-cursos.onrender.com

📊 Estructura de la Base de Datos
- **estudiantes** (id, nombre, email, fecha_creacion)
- **cursos** (id, nombre, descripcion, creditos, fecha_creacion) 
- **inscripciones** (id, estudiante_id, curso_id, fecha_inscripcion)

Relaciones:
- estudiantes ↔ inscripciones (1:N)
- cursos ↔ inscripciones (1:N)

🛠️ Instalación Local

Prerrequisitos
- Python 3.9+
- pip

Pasos de instalación

1. **Clonar el repositorio**
bash
git clone https://github.com/ozt07/Cloud08
cd Cloud08
Instalar dependencias

bash
pip install -r requirements.txt
Configurar variables de entorno
Crear archivo .env:

env
SUPABASE_URL=https://vykgdjbpsqdqjtfrivzh.supabase.co
SUPABASE_KEY=sb_publishable_0_lgoaqQNFvkBumC7AQzrw_e0cPxkti
Ejecutar la aplicación

bash
python main.py
📚 Endpoints Disponibles
🔍 Estudiantes
GET /estudiantes
Obtener todos los estudiantes

Response:

json
[
  {
    "id": 1,
    "nombre": "Ana García",
    "email": "ana@email.com",
    "fecha_creacion": "2025-11-24T04:27:04.097972"
  }
]
GET /estudiantes/{id}
Obtener estudiante por ID

Ejemplo:

text
GET /estudiantes/1
POST /estudiantes
Crear nuevo estudiante

Request:

json
{
  "nombre": "Nuevo Estudiante",
  "email": "nuevo@email.com"
}
Response:

json
{
  "message": "Estudiante creado exitosamente",
  "data": {
    "id": "nuevo"
  }
}
PUT /estudiantes/{id}
Actualizar estudiante

Request:

json
{
  "nombre": "Nombre Actualizado",
  "email": "actualizado@email.com"
}
Response:

json
{
  "message": "Estudiante actualizado exitosamente"
}
DELETE /estudiantes/{id}
Eliminar estudiante

Response:

json
{
  "message": "Estudiante eliminado exitosamente"
}
🎯 Endpoints Generales
GET /
Estado de la API

json
{
  "message": "API de Estudiantes y Cursos funcionando!",
  "version": "1.0.0"
}
GET /health
Verificar salud de la API y conexión a BD

json
{
  "status": "healthy",
  "database": "connected",
  "tables": ["estudiantes", "cursos", "inscripciones"]
}
GET /test-db
Probar conexión con la base de datos

json
{
  "message": "Conexión exitosa a Supabase",
  "estudiantes_count": 5,
  "data": [...]
}
🧪 Pruebas para el Instructor
Ejemplos de Pruebas CRUD en Producción
1. POST - Crear Estudiante
bash
curl -X POST "https://api-estudiantes-cursos.onrender.com/estudiantes" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Estudiante Prueba", "email": "prueba@instructor.com"}'
Response esperado:

json
{
  "message": "Estudiante creado exitosamente",
  "data": {
    "id": "nuevo"
  }
}
2. GET - Obtener Todos los Estudiantes
bash
curl "https://api-estudiantes-cursos.onrender.com/estudiantes"
3. GET - Obtener Estudiante por ID
bash
curl "https://api-estudiantes-cursos.onrender.com/estudiantes/1"
4. PUT - Actualizar Estudiante
bash
curl -X PUT "https://api-estudiantes-cursos.onrender.com/estudiantes/1" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Nombre Actualizado", "email": "actualizado@email.com"}'
5. DELETE - Eliminar Estudiante
bash
curl -X DELETE "https://api-estudiantes-cursos.onrender.com/estudiantes/1"
Pruebas en Postman
Importar colección con los 5 endpoints CRUD

Configurar environment con variable base_url = https://api-estudiantes-cursos.onrender.com

Ejecutar secuencia CREATE → READ → UPDATE → DELETE

Validación de Funcionalidad
✅ Creación de nuevos registros

✅ Consulta de datos existentes

✅ Actualización de información

✅ Eliminación de registros

✅ Manejo de errores

✅ Conexión a base de datos

🔧 Variables de Entorno
SUPABASE_URL: URL de la instancia de Supabase

SUPABASE_KEY: API Key de Supabase

📁 Estructura del Proyecto
text
Cloud08/
├── main.py              # Código fuente Flask
├── requirements.txt     # Dependencias Python
├── runtime.txt         # Versión Python
├── build.sh           # Script build
├── start.sh           # Script inicio
├── .env.example       # Variables ejemplo
├── README.md          # Documentación completa
└── Imagenes/          # Capturas de pruebas
🔗 Enlaces Importantes
🗂️ Repositorio GitHub: https://github.com/ozt07/Cloud08

🌐 API en Producción: https://api-estudiantes-cursos.onrender.com

🗄️ Base de Datos: https://vykgdjbpsqdqjtfrivzh.supabase.co

📚 Documentación Supabase: https://supabase.com/docs

🐍 Documentación Flask: https://flask.palletsprojects.com/

✅ Estado del Proyecto
COMPLETADO - Todos los requisitos cumplidos:

✅ API REST con endpoints CRUD completos

✅ Conexión a base de datos Supabase funcionando

✅ Despliegue en Render accesible públicamente

✅ Documentación completa con ejemplos

✅ Pruebas CRUD exitosas en producción

✅ Código fuente en GitHub

✅ Variables de entorno configuradas
