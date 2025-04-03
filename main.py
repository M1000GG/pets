from fastapi import FastAPI
from controller.pet_controller import router as pet_router

app = FastAPI()
app.include_router(pet_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
