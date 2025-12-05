from tree_design import *

def test_manual_construction():
    print("Construção Manual")
    print("#" * 60)
    root = DecisionNode("Nó Decisão 1 (Raiz)")
    
    left = DecisionNode("Nó Decisão 2 (Esq)")
    left.add_child(LeafNode("Folha A"))
    left.add_child(LeafNode("Folha B"))
    
    right = LeafNode("Classe C (Dir)")
    
    root.add_child(left)
    root.add_child(right)

    print("\nNavegando na árvore:")
    for node in root:
        print(f"{node}")

    print("\nContando Folhas:")
    counter = LeafCounterVisitor()
    root.accept(counter)
    print(f"Total de folhas: {counter.count}")

    print("\n[Visitor] Relatório de Regras:")
    regras = RulesReportVisitor()
    root.accept(regras)


def test_automated_builder():
    print("Construção Automática")
    print("#" * 60)
    
    builder = TreeBuilder()
    
    tree_root = builder.build_tree(max_depth=3)
    
    viz = RulesReportVisitor()
    if tree_root:
        tree_root.accept(viz)

if __name__ == "__main__":
    test_manual_construction()
    test_automated_builder()