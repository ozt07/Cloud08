from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurar Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json"
}

# ENDPOINTS CRUD PARA ESTUDIANTES

@app.route('/')
def read_root():
    return jsonify({"message": "API de Estudiantes y Cursos funcionando!", "version": "1.0.0"})

@app.route('/health')
def health_check():
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?select=*&limit=1"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return jsonify({
                "status": "healthy", 
                "database": "connected",
                "tables": ["estudiantes", "cursos", "inscripciones"]
            })
        else:
            return jsonify({
                "status": "error", 
                "database": "connection failed",
                "error": response.text
            })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "database": "connection failed",
            "error": str(e)
        })

@app.route('/test-db')
def test_database():
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?select=*&limit=5"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "message": "Conexión exitosa a Supabase",
                "estudiantes_count": len(data),
                "data": data
            })
        else:
            return jsonify({"error": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET - Obtener todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?select=*"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET - Obtener estudiante por ID
@app.route('/estudiantes/<int:estudiante_id>', methods=['GET'])
def get_estudiante(estudiante_id):
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?id=eq.{estudiante_id}&select=*"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return jsonify(data[0])
            else:
                return jsonify({"error": "Estudiante no encontrado"}), 404
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST - Crear nuevo estudiante
@app.route('/estudiantes', methods=['POST'])
def create_estudiante():
    try:
        data = request.get_json()
        if not data or 'nombre' not in data or 'email' not in data:
            return jsonify({"error": "Se requieren nombre y email"}), 400
            
        url = f"{supabase_url}/rest/v1/estudiantes"
        post_data = {
            "nombre": data['nombre'],
            "email": data['email']
        }
        
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code == 201:
            try:
                response_data = response.json() if response.text else {"id": "nuevo"}
                return jsonify({
                    "message": "Estudiante creado exitosamente", 
                    "data": response_data
                }), 201
            except:
                return jsonify({
                    "message": "Estudiante creado exitosamente", 
                    "data": {"id": "nuevo"}
                }), 201
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT - Actualizar estudiante
@app.route('/estudiante/<int:estudiante_id>', methods=['PUT'])
def update_estudiante(estudiante_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No hay datos para actualizar"}), 400
            
        url = f"{supabase_url}/rest/v1/estudiantes?id=eq.{estudiante_id}"
        
        update_data = {}
        if 'nombre' in data:
            update_data['nombre'] = data['nombre']
        if 'email' in data:
            update_data['email'] = data['email']
            
        if not update_data:
            return jsonify({"error": "No hay datos válidos para actualizar"}), 400
        
        response = requests.patch(url, headers=headers, json=update_data)
        
        if response.status_code == 204:
            return jsonify({"message": "Estudiante actualizado exitosamente"})
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE - Eliminar estudiante
@app.route('/estudiantes/<int:estudiante_id>', methods=['DELETE'])
def delete_estudiante(estudiante_id):
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?id=eq.{estudiante_id}"
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 204:
            return jsonify({"message": "Estudiante eliminado exitosamente"})
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)