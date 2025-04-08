from model.pet import Pet
from model.abb import ABB
from typing import List, Dict, Optional
import os


class ABBService:
    def __init__(self):
        self.abb = ABB()
        self.messages = self._load_messages()

    def _load_messages(self):
        messages = {}
        try:
            # Intentar con diferentes codificaciones
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

    def add(self, data: Pet):
        if not data.name or data.name.strip() == "":
            raise Exception(self.messages["pet_empty_name"])

        if data.age < 0:
            raise Exception(self.messages["pet_invalid_age"])

        if data.id <= 0:
            raise Exception(self.messages["pet_invalid_id"])

        if not data.breed or data.breed.strip() == "":
            raise Exception(self.messages["invalid_breed"])

        if self.abb.exists(data.id):
            raise Exception(self.messages["pet_duplicate_id"])

        self.abb.add(data)

    def update(self, id: int, data: Pet) -> bool:
        if id <= 0:
            raise Exception(self.messages["pet_invalid_id"])

        if not data.name or data.name.strip() == "":
            raise Exception(self.messages["pet_empty_name"])

        if data.age < 0:
            raise Exception(self.messages["pet_invalid_age"])

        if not data.breed or data.breed.strip() == "":
            raise Exception(self.messages["invalid_breed"])

        return self.abb.update(id, data)

    def get(self, id: int) -> Optional[Pet]:
        if id <= 0:
            raise Exception(self.messages["pet_invalid_id"])

        return self.abb.get(id)

    def get_all(self) -> List[Pet]:
        return self.abb.get_all()

    def delete(self, id: int) -> bool:
        if id <= 0:
            raise Exception(self.messages["pet_invalid_id"])

        return self.abb.delete(id)

    def count_breeds(self) -> Dict[str, int]:
        return self.abb.count_breeds()

    def exists(self, id: int) -> bool:
        if id <= 0:
            raise Exception(self.messages["pet_invalid_id"])

        return self.abb.exists(id)

    def get_inorden(self) -> List[Pet]:
        return self.abb.get_inorden()

    def get_preorden(self) -> List[Pet]:
        return self.abb.get_preorden()

    def get_postorden(self) -> List[Pet]:
        return self.abb.get_postorden()