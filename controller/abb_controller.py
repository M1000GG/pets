from fastapi import APIRouter, HTTPException, Path, Body
from model.pet import Pet
from service.abb_service import ABBService
import os


class ABBController:
    def __init__(self):
        self.router = APIRouter()
        self.abb_service = ABBService()
        self.messages = self._load_messages()
        self._setup_routes()

    def _load_messages(self):
        messages = {}
        try:
            encodings = ['utf-8', 'latin-1', 'cp1252']

            for encoding in encodings:
                try:
                    with open(os.path.join("config", "messages.properties"), "r", encoding=encoding) as f:
                        for line in f:
                            if "=" in line and not line.strip().startswith("#"):
                                key, value = line.strip().split("=", 1)
                                messages[key] = value
                    break
                except UnicodeDecodeError:
                    continue

            return messages
        except Exception as e:
            print(f"Error loading messages: {str(e)}")
            return {}

    def _setup_routes(self):

        @self.router.get("/pets")
        def get_all_pets():
            try:
                pets = self.abb_service.get_all()
                if not pets:
                    return {"message": self.messages["no_pets_found"], "pets": []}
                return {"pets": [pet.to_dict() for pet in pets]}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.post("/pet")
        def create_pet(pet_data: dict = Body(...)):
            try:
                id = pet_data.get("id")
                name = pet_data.get("name")
                age = pet_data.get("age")
                breed = pet_data.get("breed")

                if id is None or name is None or age is None or breed is None:
                    raise HTTPException(status_code=400, detail="Datos de mascota incompletos")

                new_pet = Pet(id=id, name=name, age=age, breed=breed)
                self.abb_service.add(new_pet)
                return {"message": self.messages["pet_created"], "pet": new_pet.to_dict()}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.put("/pet/{id}")
        def update_pet(id: int = Path(...), pet_data: dict = Body(...)):
            try:
                name = pet_data.get("name")
                age = pet_data.get("age")
                breed = pet_data.get("breed")

                if name is None or age is None or breed is None:
                    raise HTTPException(status_code=400, detail="Datos de mascota incompletos")

                updated_pet = Pet(id=id, name=name, age=age, breed=breed)
                result = self.abb_service.update(id, updated_pet)

                if not result:
                    raise HTTPException(status_code=404, detail=self.messages["pet_not_found"])

                return {"message": self.messages["pet_updated"], "pet": updated_pet.to_dict()}
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.get("/pet/{id}")
        def get_pet(id: int = Path(...)):
            try:
                pet = self.abb_service.get(id)
                if pet is None:
                    raise HTTPException(status_code=404, detail=self.messages["pet_not_found"])
                return {"pet": pet.to_dict()}
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.delete("/pet/{id}")
        def delete_pet(id: int = Path(...)):
            try:
                result = self.abb_service.delete(id)
                if not result:
                    raise HTTPException(status_code=404, detail=self.messages["pet_not_found"])
                return {"message": self.messages["pet_deleted"]}
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.get("/breeds/count")
        def count_breeds():
            try:
                breeds = self.abb_service.count_breeds()
                if not breeds:
                    return {"message": self.messages["no_pets_found"], "breeds": {}}
                return {"breeds": breeds}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.get("/pet/exists/{id}")
        def exists_pet(id: int = Path(...)):
            try:
                result = self.abb_service.exists(id)
                return {"exists": result}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.get("/pets/inorden")
        def get_inorden():
            try:
                pets = self.abb_service.get_inorden()
                if not pets:
                    return []
                return [pet.to_dict() for pet in pets]  # Retorna directamente la lista
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.get("/pets/preorden")
        def get_preorden():
            try:
                pets = self.abb_service.get_preorden()
                if not pets:
                    return []
                return [pet.to_dict() for pet in pets]  # Retorna directamente la lista
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.get("/pets/postorden")
        def get_postorden():
            try:
                pets = self.abb_service.get_postorden()
                if not pets:
                    return []
                return [pet.to_dict() for pet in pets]  # Retorna directamente la lista
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
