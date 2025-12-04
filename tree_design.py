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


class NodeVisitor(ABC):
    """
    Interface Visitor: Declara métodos de visita para cada tipo concreto de elemento.
    """
    @abstractmethod
    def visit_decision_node(self, node: DecisionNode) -> None: ...

    @abstractmethod
    def visit_leaf_node(self, node: LeafNode) -> None: ...


class LeafCounterVisitor(NodeVisitor):
    """
    Visitor que percorre a árvore para contar quantos nós folhas existem.
    """
    def __init__(self) -> None:
        self.count = 0

    def visit_decision_node(self, node: DecisionNode) -> None:
        for child in node.get_children():
            child.accept(self)

    def visit_leaf_node(self, node: LeafNode) -> None:
        print(f"[Visitor] Folha encontrada: {node.value}")
        self.count += 1


class RulesReportVisitor(NodeVisitor):
    """
    Visitor que extrai apenas as regras de decisão
    """
    def visit_decision_node(self, node: DecisionNode) -> None:
        print(f"[Relatório] Regra de Decisão Identificada: '{node.condition}'")
        for child in node.get_children():
            child.accept(self)

    def visit_leaf_node(self, node: LeafNode) -> None:
        pass


###############################################################


class Node(ABC):
    """
    Componente base do padrão Composite.
    """
        
    @abstractmethod
    def add_child(self, child: Node) -> None: ...

    # Método pro visitor
    @abstractmethod
    def accept(self, visitor: NodeVisitor) -> None: ...

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
    
    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_decision_node(self)
    
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

    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_leaf_node(self)
    
    def __str__(self) -> str:
        return f"[Leaf] Resultado: {self.value}"