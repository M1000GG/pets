class Pet:
    def __init__(self, id: int, name: str, age: int, breed: str):
        self.id = id
        self.name = name
        self.age = age
        self.breed = breed

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "breed": self.breed
        }