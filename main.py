from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.abb_controller import ABBController
import uvicorn

app = FastAPI()

# Inicializar el controlador y registrar las rutas
controller = ABBController()
app.include_router(controller.router, prefix="/api", tags=["pets"])

# Ruta raíz
@app.get("/", tags=["root"])
def read_root():
    return {"message": "Bienvenido a la API de gestión de mascotas"}

# Iniciar la aplicación cuando se ejecuta directamente
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)