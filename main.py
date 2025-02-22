from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Pet(BaseModel):
    id: int
    name: str
    age: int
    type: str
    owner: Optional[str]

pets = []


@app.post("/pets/", response_model=Pet)
def create_pet(pet: Pet):
    for p in pets:
        if p.id == pet.id:
            raise HTTPException(status_code=400, detail="Este ID ya fue creado.")
    pets.append(pet)
    return pet


@app.get("/pets/", response_model=List[Pet])
def get_pets():
    return pets


@app.get("/pets/{pet_id}", response_model=Pet)
def get_pet(pet_id: int):
    for pet in pets:
        if pet.id == pet_id:
            return pet
    raise HTTPException(status_code=404, detail="Mascota no encontrada.")


@app.put("/pets/{pet_id}", response_model=Pet)
def update_pet(pet_id: int, updated_pet: Pet):
    for pet in pets:
        if pet.id == pet_id:
            pet.name = updated_pet.name
            pet.age = updated_pet.age
            pet.type = updated_pet.type
            pet.owner = updated_pet.owner
            return pet
    raise HTTPException(status_code=404, detail="Mascota no encontrada.")


@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int):
    for pet in pets:
        if pet.id == pet_id:
            pets.remove(pet)
            return {"Aviso": "Mascota eliminada correctamente"}
    raise HTTPException(status_code=404, detail="Mascota no encontrada.")