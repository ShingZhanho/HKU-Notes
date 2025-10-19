from __future__ import annotations

class KeyNode:
    """
    A node representing a key in a hierarchical structure.
    All key nodes should inherit from this class and define their children keys or values as attributes.
    This class itself should not be instantiated directly.
    """
    def __init__(self, parent_node: KeyNode | None = None):
        if parent_node is not None and not isinstance(parent_node, KeyNode):
            raise TypeError("parent_node must be a KeyNode or None")
        self.parent = parent_node