from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Any

class Node(ABC):
    """
    Componente base do padrão Composite.
    """
        
    @abstractmethod
    def add_child(self, child: Node) -> None: ...

class DecisionNode(Node):
    """
    Composite: Nó interno que contém filhos e uma condição de decisão.
    """
    def __init__(self) -> None:
        self._children: List[Node] = []
    
    def add_child(self, child: Node) -> None: 
        print("Criando Nó Filho")

    def get_children(self) -> List[Node]: ...

class LeafNode(Node):
    """
    Leaf: Nó folha que representa o resultado final (classe ou valor).
    """
    def __init__(self, value: Any) -> None:
        self.value = value
    
    def add_child(self, child: Node) -> None:
        print("Nós folhas não tem filhos!")
        ...