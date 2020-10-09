
from ml_workflow.workflow import WorkflowNode

def test_constructor_polymorphism():
    root = WorkflowNode(None)
    child = WorkflowNode(None, parents = root)
    assert(child.parents == [root])
    child = WorkflowNode(None, parents = [root])
    assert(child.parents == [root])

def test_graph_size():
    root1 = WorkflowNode(None)
    root2 = WorkflowNode(None)

    child1 = WorkflowNode(None, parents = root2)
    merge_child2 = WorkflowNode(None, parents = [root1, child1])
    child3 = WorkflowNode(None, parents = merge_child2)

    assert(root1.get_graph_size() == 1)
    assert(root2.get_graph_size() == 1)
    assert(child1.get_graph_size() == 2)
    assert(merge_child2.get_graph_size() == 4)
    assert(child3.get_graph_size() == 5)
