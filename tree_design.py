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
    

##############################################################################

class BuilderState(ABC):
    """
    Interface State: Define o comportamento abstrato para os estados de construção.
    """
    @abstractmethod
    def handle(self, builder: TreeBuilder, depth: int, max_depth: int) -> Node: ...


class TreeBuilder:
    """
    Context do padrão State. Mantém a referência para o estado atual.
    """
    def __init__(self) -> None:
        self._state: BuilderState = SplittingState()
        
    def set_state(self, state: BuilderState) -> None:
        print(f"[State Change] {type(self._state).__name__} -> {type(state).__name__}")
        self._state = state
        
    def build_tree(self, max_depth: int) -> Node:
        print(f"--- Iniciando Construção (Max Depth: {max_depth}) ---")
        return self._state.handle(self, current_depth=0, max_depth=max_depth)


class SplittingState(BuilderState):
    """
    Estado de Divisão.
    """
    def handle(self, builder: TreeBuilder, current_depth: int, max_depth: int) -> Node:
        
        if current_depth >= max_depth:
            print(f"[Splitting] Profundidade {current_depth} atingida. Mudando para Stopping.")
            builder.set_state(StoppingState())
            return builder._state.handle(builder, current_depth, max_depth)
        
        print(f"[Splitting] Criando nó na profundidade {current_depth}...")
        node = DecisionNode(f"Feature_X > {current_depth * 10}")
        
        left_child = builder._state.handle(builder, current_depth + 1, max_depth)
        right_child = builder._state.handle(builder, current_depth + 1, max_depth)
        
        node.add_child(left_child)
        node.add_child(right_child)
        
        return node


class StoppingState(BuilderState):
    """
    Estado de Parada.
    """
    def handle(self, builder: TreeBuilder, current_depth: int, max_depth: int) -> Node:
        return LeafNode(value=f"Classe_{current_depth}")


class PruningState(BuilderState):
    def handle(self, builder: TreeBuilder, current_depth: int, max_depth: int) -> Node:
        return LeafNode("Podada")