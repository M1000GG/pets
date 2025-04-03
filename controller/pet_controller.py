from fastapi import APIRouter, HTTPException
from model.abb_model import BinarySearchTree
from model.pet_model import Pet
from typing import List

router = APIRouter()
bst = BinarySearchTree()

@router.post("/pets/", response_model=Pet)
def create_pet(pet: Pet):
    try:
        bst.insert(pet)
        return pet
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/pets/", response_model=List[Pet])
def get_pets():
    return bst.get_all_pets()

@router.get("/pets/average-age")
def age_average():
    pets = bst.get_all_pets()
    if not pets:
        raise HTTPException(status_code=400, detail="No hay mascotas registradas.")
    return {"Promedio de edad": round(sum(pet.age for pet in pets) / len(pets), 2)}

@router.get("/pets/count-by-race")
def count_by_race():
    return bst.count_by_race()

@router.get("/pets/{pet_id}", response_model=Pet)
def get_pet(pet_id: int):
    pet = bst.search(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada.")
    return pet

@router.put("/pets/{pet_id}", response_model=Pet)
def update_pet(pet_id: int, updated_pet: Pet):
    pet = bst.search(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada.")
    pet.name, pet.age, pet.race = updated_pet.name, updated_pet.age, updated_pet.race
    return pet

@router.delete("/pets/{pet_id}")
def delete_pet(pet_id: int):
    if not bst.delete(pet_id):
        raise HTTPException(status_code=404, detail="Mascota no encontrada.")
    return {"message": "Mascota eliminada correctamente"}
