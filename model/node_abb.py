from model.pet import Pet
from typing import List, Dict, Optional


class NodeABB:
    def __init__(self, data: Pet):
        self.data = data
        self.left = None
        self.right = None

    def add(self, data: Pet):
        if data.id < self.data.id:
            if self.left is None:
                self.left = NodeABB(data)
            else:
                self.left.add(data)
        elif data.id > self.data.id:
            if self.right is None:
                self.right = NodeABB(data)
            else:
                self.right.add(data)
        else:
            raise Exception("Ya existe una mascota con ese ID")

    def update(self, id: int, data: Pet) -> bool:
        if self.data.id == id:
            self.data.name = data.name
            self.data.age = data.age
            self.data.breed = data.breed
            return True
        elif id < self.data.id and self.left is not None:
            return self.left.update(id, data)
        elif id > self.data.id and self.right is not None:
            return self.right.update(id, data)
        return False

    def get(self, id: int) -> Optional[Pet]:
        if self.data.id == id:
            return self.data
        elif id < self.data.id and self.left is not None:
            return self.left.get(id)
        elif id > self.data.id and self.right is not None:
            return self.right.get(id)
        return None

    def delete(self, id: int) -> Optional['NodeABB']:
        if id < self.data.id:
            if self.left:
                self.left = self.left.delete(id)
            return self
        elif id > self.data.id:
            if self.right:
                self.right = self.right.delete(id)
            return self
        else:
            if self.left is None and self.right is None:
                return None
            elif self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            else:
                successor = self._find_min_node(self.right)
                self.data = successor.data
                self.right = self.right.delete(successor.data.id)
                return self

    def _find_min_node(self, node: 'NodeABB') -> 'NodeABB':
        current = node
        while current.left is not None:
            current = current.left
        return current

    def count_breeds(self) -> Dict[str, int]:
        breeds = {}

        if self.data.breed in breeds:
            breeds[self.data.breed] += 1
        else:
            breeds[self.data.breed] = 1

        if self.left:
            left_breeds = self.left.count_breeds()
            for breed, count in left_breeds.items():
                if breed in breeds:
                    breeds[breed] += count
                else:
                    breeds[breed] = count

        if self.right:
            right_breeds = self.right.count_breeds()
            for breed, count in right_breeds.items():
                if breed in breeds:
                    breeds[breed] += count
                else:
                    breeds[breed] = count

        return breeds

    def exists(self, id: int) -> bool:
        if self.data.id == id:
            return True
        elif id < self.data.id and self.left is not None:
            return self.left.exists(id)
        elif id > self.data.id and self.right is not None:
            return self.right.exists(id)
        return False

    def get_inorden(self) -> List[Pet]:
        result = []
        if self.left:
            result.extend(self.left.get_inorden())
        result.append(self.data)
        if self.right:
            result.extend(self.right.get_inorden())
        return result

    def get_preorden(self) -> List[Pet]:
        result = [self.data]
        if self.left:
            result.extend(self.left.get_preorden())
        if self.right:
            result.extend(self.right.get_preorden())
        return result

    def get_postorden(self) -> List[Pet]:
        result = []
        if self.left:
            result.extend(self.left.get_postorden())
        if self.right:
            result.extend(self.right.get_postorden())
        result.append(self.data)
        return result