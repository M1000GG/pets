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
        if self.root is None:
            self.root = TreeNode(pet)
        else:
            self._insert_recursive(self.root, pet)

    def _insert_recursive(self, node, pet: Pet):
        if pet.id < node.pet.id:
            if node.left is None:
                node.left = TreeNode(pet)
            else:
                self._insert_recursive(node.left, pet)
        elif pet.id > node.pet.id:
            if node.right is None:
                node.right = TreeNode(pet)
            else:
                self._insert_recursive(node.right, pet)
        else:
            raise ValueError("El ID ya existe en el árbol.")

    def search(self, pet_id: int):
        return self._search_recursive(self.root, pet_id)

    def _search_recursive(self, node, pet_id: int):
        if node is None:
            return None
        if pet_id == node.pet.id:
            return node.pet
        elif pet_id < node.pet.id:
            return self._search_recursive(node.left, pet_id)
        else:
            return self._search_recursive(node.right, pet_id)

    def delete(self, pet_id: int):
        self.root, deleted = self._delete_recursive(self.root, pet_id)
        return deleted

    def _delete_recursive(self, node, pet_id: int):
        if node is None:
            return node, False
        if pet_id < node.pet.id:
            node.left, deleted = self._delete_recursive(node.left, pet_id)
        elif pet_id > node.pet.id:
            node.right, deleted = self._delete_recursive(node.right, pet_id)
        else:
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True

            min_larger_node = self._get_min(node.right)
            node.pet = min_larger_node.pet
            node.right, _ = self._delete_recursive(node.right, min_larger_node.pet.id)
            return node, True
        return node, deleted

    def _get_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def get_all_pets(self):
        pets = []
        self._in_order_traversal(self.root, pets)
        return pets

    def _in_order_traversal(self, node, pets):
        if node is not None:
            self._in_order_traversal(node.left, pets)
            pets.append(node.pet)
            self._in_order_traversal(node.right, pets)

    def count_by_race(self):
        race_count = defaultdict(int)
        self._count_race_recursive(self.root, race_count)
        return dict(race_count)

    def _count_race_recursive(self, node, race_count):
        if node is not None:
            race_count[node.pet.race] += 1
            self._count_race_recursive(node.left, race_count)
            self._count_race_recursive(node.right, race_count)
