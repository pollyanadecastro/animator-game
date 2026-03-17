from tree.node import Node


class AVL:
    def __init__(self):
        self.root = None

    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.yes), self._height(node.no))

    def _balance_factor(self, node):
        return self._height(node.yes) - self._height(node.no)

    def _rotate_right(self, y):
        x     = y.yes
        T2    = x.no
        x.no  = y
        y.yes = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y     = x.no
        T2    = y.yes
        y.yes = x
        x.no  = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _get_key(self, node):
        return node.question if node.question else node.answer

    def _insert(self, root, new_node):
        if root is None:
            return new_node

        if self._get_key(new_node) < self._get_key(root):
            root.yes = self._insert(root.yes, new_node)
        elif self._get_key(new_node) > self._get_key(root):
            root.no  = self._insert(root.no,  new_node)
        else:
            return root

        self._update_height(root)
        bf = self._balance_factor(root)

        if bf > 1 and self._get_key(new_node) < self._get_key(root.yes):
            return self._rotate_right(root)

        if bf < -1 and self._get_key(new_node) > self._get_key(root.no):
            return self._rotate_left(root)

        if bf > 1 and self._get_key(new_node) > self._get_key(root.yes):
            root.yes = self._rotate_left(root.yes)
            return self._rotate_right(root)

        if bf < -1 and self._get_key(new_node) < self._get_key(root.no):
            root.no = self._rotate_right(root.no)
            return self._rotate_left(root)

        return root

    def insert(self, node):
        self.root = self._insert(self.root, node)

    def get_root(self):
        return self.root

    def get_height(self):
        return self._height(self.root)

    def count_nodes(self):
        def _count(node):
            if node is None:
                return 0
            return 1 + _count(node.yes) + _count(node.no)
        return _count(self.root)

    def __repr__(self):
        return f"AVL(root={self.root}, height={self._height(self.root)})"
