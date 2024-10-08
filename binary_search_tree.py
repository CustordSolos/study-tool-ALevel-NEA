from anytree import NodeMixin
from anytree.exporter import DotExporter
from pathlib import Path
from merge_sort import MergeSort
from typing import List

"""
Generates binary search trees alongside their traversals
"""


class BinarySearchTreeNode(NodeMixin):
    """Class representing nodes in a binary search tree."""

    def __init__(self, value: int, parent: "BinarySearchTreeNode" = None) -> None:
        """
        Initialise a BinarySearchTreeNode object.

        Arguments:
            value (int): Value of the node.
            parent (BinarySearchTreeNode): Reference to the parent node. Defaults to None.
        """
        super().__init__()
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    @property
    def children(self) -> List["BinarySearchTreeNode"]:
        """Return a list of children nodes."""
        return [node for node in (self.left, self.right) if node is not None]


class BinarySearchTree:
    """Class representing a binary search tree."""

    def __init__(self) -> None:
        """Initialise an empty binary search tree."""
        self.root = None

    def add_node(self, value: int) -> None:
        """
        Add a node to the tree.

        Arguments:
            value (int): Value to be assigned to the node attribute.
        """
        if not self.root:
            self.root = BinarySearchTreeNode(value)
        else:
            self._add_node_recursive(self.root, value)

    def _add_node_recursive(
        self, current_node: BinarySearchTreeNode, value: int
    ) -> None:
        """
        Recursively navigate the tree to correctly insert a new node.

        Arguments:
            current_node (BinarySearchTreeNode): Current node for recursive process.
            value (int): Value to be assigned to the new node.
        """
        if value < current_node.value:
            if current_node.left is None:
                current_node.left = BinarySearchTreeNode(value, parent=current_node)
            else:
                self._add_node_recursive(current_node.left, value)
        elif value > current_node.value:
            if current_node.right is None:
                current_node.right = BinarySearchTreeNode(value, parent=current_node)
            else:
                self._add_node_recursive(current_node.right, value)

    def build_tree(self, values: List[int]) -> None:
        """Build a tree from a list of values."""
        for value in values:
            self.add_node(value)

    def render_as_image(self, filename: str = "binary_search_tree") -> Path:
        """
        Export the tree as a PNG image using DotExporter.

        Arguments:
            filename: Name of the image file. Defaults to "binary_search_tree".

        Returns:
            Path: File path where the image was saved.
        """
        if not self.root:
            return
        file_path = Path.cwd() / "assets" / f"{filename}.png"
        DotExporter(self.root, nodenamefunc=lambda n: str(n.value)).to_picture(
            file_path
        )
        return file_path

    def pre_order_traversal(self, node: BinarySearchTreeNode = None) -> List[int]:
        """
        Return pre-order traversal of the tree.

        Arguments:
            node: Optional parameter, references a node object.

        Returns:
            List[int]: Node values in order of pre-order traversal.
        """
        if node is None:
            node = self.root
        result = [node.value]
        if node.left:
            result.extend(self.pre_order_traversal(node.left))
        if node.right:
            result.extend(self.pre_order_traversal(node.right))
        return result

    def in_order_traversal(self, node: BinarySearchTreeNode = None) -> List[int]:
        """
        Return in-order traversal of the tree.

        Arguments:
            node: Optional parameter, references a node object.

        Returns:
            List[int]: Node values in order of in-order traversal.
        """
        if node is None:
            node = self.root
        result = []
        if node.left:
            result.extend(self.in_order_traversal(node.left))
        result.append(node.value)
        if node.right:
            result.extend(self.in_order_traversal(node.right))
        return result

    def post_order_traversal(self, node: BinarySearchTreeNode = None) -> List[int]:
        """
        Return post-order traversal of the tree.

        Arguments:
            node: Optional parameter, references a node object.

        Returns:
            List[int]: Node values in order of post-order traversal.
        """
        if node is None:
            node = self.root
        result = []
        if node.left:
            result.extend(self.post_order_traversal(node.left))
        if node.right:
            result.extend(self.post_order_traversal(node.right))
        result.append(node.value)
        return result

    def build_balanced_tree(self, values: List[int]) -> None:
        """
        Build a balanced tree from a sorted list of values.

        Arguments:
            values (List[int]): Sorted list of values.
        """
        values = list(set(values))
        sorted_values = MergeSort.sort(values)
        self.root = self._build_balanced_tree_recursive(sorted_values)

    def _build_balanced_tree_recursive(self, values: List[int]) -> BinarySearchTreeNode:
        """
        Recursive method for building a balanced tree from a sorted list of values.

        Arguments:
            values (List[int]): Sorted list of values.

        Returns:
            BinarySearchTreeNode: Root node of the balanced tree.
        """
        if not values:
            return None
        mid_index = len(values) // 2
        root_value = values[mid_index]
        root = BinarySearchTreeNode(root_value)
        root.left = self._build_balanced_tree_recursive(values[:mid_index])
        root.right = self._build_balanced_tree_recursive(values[mid_index + 1 :])
        return root
