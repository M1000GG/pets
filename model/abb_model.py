from model.pet_model import Pet
from collections import defaultdict

class TreeNode:
    def __init__(self, pet: Pet):
        self.pet = pet
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, pet: Pet):
        if not self.root:
            self.root = TreeNode(pet)
        else:
            self._insert(self.root, pet)

    def _insert(self, node, pet: Pet):
        if pet.id < node.pet.id:
            if node.left:
                self._insert(node.left, pet)
            else:
                node.left = TreeNode(pet)
        elif pet.id > node.pet.id:
            if node.right:
                self._insert(node.right, pet)
            else:
                node.right = TreeNode(pet)
        else:
            raise ValueError("El ID ya existe.")

    def search(self, pet_id: int):
        return self._search(self.root, pet_id)

    def _search(self, node, pet_id: int):
        if not node or node.pet.id == pet_id:
            return node.pet if node else None
        return self._search(node.left, pet_id) if pet_id < node.pet.id else self._search(node.right, pet_id)

    def delete(self, pet_id: int):
        self.root, deleted = self._delete(self.root, pet_id)
        return deleted

    def _delete(self, node, pet_id: int):
        if not node:
            return node, False
        if pet_id < node.pet.id:
            node.left, deleted = self._delete(node.left, pet_id)
        elif pet_id > node.pet.id:
            node.right, deleted = self._delete(node.right, pet_id)
        else:
            if not node.left:
                return node.right, True
            if not node.right:
                return node.left, True
            min_larger_node = self._get_min(node.right)
            node.pet = min_larger_node.pet
            node.right, _ = self._delete(node.right, min_larger_node.pet.id)
            return node, True
        return node, deleted

    def _get_min(self, node):
        while node.left:
            node = node.left
        return node

    def get_all_pets(self):
        pets = []
        self._in_order(self.root, pets)
        return pets

    def _in_order(self, node, pets):
        if node:
            self._in_order(node.left, pets)
            pets.append(node.pet)
            self._in_order(node.right, pets)

    def count_by_race(self):
        race_count = defaultdict(int)
        self._count_race(self.root, race_count)
        return dict(race_count)

    def _count_race(self, node, race_count):
        if node:
            race_count[node.pet.race] += 1
            self._count_race(node.left, race_count)
            self._count_race(node.right, race_count)
