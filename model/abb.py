from model.pet import Pet
from model.node_abb import NodeABB
from typing import List, Dict, Optional


class ABB:
    def __init__(self):
        self.root = None

    def add(self, data: Pet):
        if self.root is None:
            self.root = NodeABB(data)
        else:
            self.root.add(data)

    def update(self, id: int, data: Pet) -> bool:
        if self.root is None:
            return False
        return self.root.update(id, data)

    def get(self, id: int) -> Optional[Pet]:
        if self.root is None:
            return None
        return self.root.get(id)

    def get_all(self) -> List[Pet]:
        return self.get_inorden()

    def delete(self, id: int) -> bool:
        if self.root is None:
            return False

        if not self.exists(id):
            return False

        self.root = self.root.delete(id)
        return True

    def count_breeds(self) -> Dict[str, int]:
        if self.root is None:
            return {}
        return self.root.count_breeds()

    def exists(self, id: int) -> bool:
        if self.root is None:
            return False
        return self.root.exists(id)

    def get_inorden(self) -> List[Pet]:
        if self.root is None:
            return []
        return self.root.get_inorden()

    def get_preorden(self) -> List[Pet]:
        if self.root is None:
            return []
        return self.root.get_preorden()

    def get_postorden(self) -> List[Pet]:
        if self.root is None:
            return []
        return self.root.get_postorden()