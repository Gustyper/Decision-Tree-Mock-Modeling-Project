from tree_design import* 

root = DecisionNode("Nó Decisão 1")

left = DecisionNode("Nó Decisão 2")
left.add_child(LeafNode("Folha A"))
left.add_child(LeafNode("Folha B"))

right = LeafNode("Classe C")

root.add_child(left)
root.add_child(right)

for node in root:
    print(node)