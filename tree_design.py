from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class TreeIterator(ABC):
    @abstractmethod
    def __next__(self) -> Node: ...
    
    @abstractmethod
    def __iter__(self) -> TreeIterator: ...

class PreOrderIterator(TreeIterator):
    """
    Iterador Pre-Order (DFS): Visita o nó atual, depois seus filhos.
    """
    def __init__(self, root: Node) -> None:
        self._stack: List[Node] = [root] if root else []

    def __iter__(self) -> TreeIterator:
        return self

    def __next__(self) -> Node:
        if not self._stack:
            raise StopIteration
        
        current_node = self._stack.pop()
        
        if isinstance(current_node, DecisionNode):
            children = current_node.get_children()
            for child in reversed(children):
                self._stack.append(child)
                
        return current_node


###############################################################  


class Node(ABC):
    """
    Componente base do padrão Composite.
    """
        
    @abstractmethod
    def add_child(self, child: Node) -> None: ...

    @abstractmethod
    def __str__(self) -> str: ...

    def __iter__(self) -> TreeIterator:
        return PreOrderIterator(self)


class DecisionNode(Node):
    """
    Composite: Nó interno que contém filhos e uma condição de decisão.
    """
    def __init__(self, condition: str) -> None:
        self.condition = condition
        self._children: List[Node] = []
    
    def add_child(self, child: Node) -> None: 
        self._children.append(child)

    def get_children(self) -> List[Node]: 
        return self._children
    
    def __str__(self) -> str:
        return f"[Decision] {self.condition}"

class LeafNode(Node):
    """
    Leaf: Nó folha que representa o resultado final.
    """
    def __init__(self, value: Any) -> None:
        self.value = value
    
    def add_child(self, child: Node) -> None:
        print(f"[Warn] Tentativa de adicionar filho em Folha: {self.value}")
    
    def __str__(self) -> str:
        return f"[Leaf] Resultado: {self.value}"