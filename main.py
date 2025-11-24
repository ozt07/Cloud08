from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
import requests
import json

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="API Estudiantes y Cursos",
    description="API REST para gestionar estudiantes, cursos e inscripciones",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json"
}

# Modelos Pydantic
class EstudianteBase(BaseModel):
    nombre: str
    email: str

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None

# ENDPOINTS CRUD PARA ESTUDIANTES

# GET - Obtener todos los estudiantes
@app.get("/estudiantes", response_model=List[dict])
def get_estudiantes():
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?select=*"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# GET - Obtener estudiante por ID
@app.get("/estudiantes/{estudiante_id}")
def get_estudiante(estudiante_id: int):
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?id=eq.{estudiante_id}&select=*"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
            else:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# POST - Crear nuevo estudiante
@app.post("/estudiantes", status_code=status.HTTP_201_CREATED)
def create_estudiante(estudiante: EstudianteCreate):
    try:
        url = f"{supabase_url}/rest/v1/estudiantes"
        data = {
            "nombre": estudiante.nombre,
            "email": estudiante.email
        }
        
        print(f"🔍 DEBUG POST:")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {data}")
        
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 201:
            try:
                response_data = response.json() if response.text else {"id": "nuevo"}
                return {"message": "Estudiante creado exitosamente", "data": response_data}
            except:
                return {"message": "Estudiante creado exitosamente", "data": {"id": "nuevo"}}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error completo: {str(e)}")

# PUT - Actualizar estudiante
@app.put("/estudiantes/{estudiante_id}")
def update_estudiante(estudiante_id: int, estudiante: EstudianteUpdate):
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?id=eq.{estudiante_id}"
        
        # Filtrar campos no nulos
        update_data = {}
        if estudiante.nombre is not None:
            update_data["nombre"] = estudiante.nombre
        if estudiante.email is not None:
            update_data["email"] = estudiante.email
            
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        print(f"🔍 DEBUG PUT:")
        print(f"URL: {url}")
        print(f"Update Data: {update_data}")
        
        response = requests.patch(url, headers=headers, json=update_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 204:
            return {"message": "Estudiante actualizado exitosamente"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error completo: {str(e)}")

# DELETE - Eliminar estudiante
@app.delete("/estudiantes/{estudiante_id}")
def delete_estudiante(estudiante_id: int):
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?id=eq.{estudiante_id}"
        
        print(f"🔍 DEBUG DELETE:")
        print(f"URL: {url}")
        
        response = requests.delete(url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 204:
            return {"message": "Estudiante eliminado exitosamente"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error completo: {str(e)}")

# Endpoints básicos (mantener los existentes)
@app.get("/")
def read_root():
    return {"message": "API de Estudiantes y Cursos funcionando!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?select=*&limit=1"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return {
                "status": "healthy", 
                "database": "connected",
                "tables": ["estudiantes", "cursos", "inscripciones"]
            }
        else:
            return {
                "status": "error", 
                "database": "connection failed",
                "error": response.text
            }
    except Exception as e:
        return {
            "status": "error", 
            "database": "connection failed",
            "error": str(e)
        }

@app.get("/test-db")
def test_database():
    try:
        url = f"{supabase_url}/rest/v1/estudiantes?select=*&limit=5"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "message": "Conexión exitosa a Supabase",
                "estudiantes_count": len(data),
                "data": data
            }
        else:
            raise HTTPException(status_code=500, detail=f"Error en la consulta: {response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la conexión: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)