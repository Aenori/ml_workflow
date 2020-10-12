from common_import import *

from fixtures import simple_graph_factory

def get_simple_fork_network():
    root1 = WorkflowNode('DataSource1')
    root2 = WorkflowNode('DataSource2')

    child1 = WorkflowNode('Processing_on_DS2', parents = root2)
    merge_child2 = WorkflowNode('Merge_sources', parents = [root1, child1])
    child3 = WorkflowNode('LeafNode', parents = merge_child2)

    return root1, root2, child1, merge_child2, child3

def test_constructor_polymorphism():
    root = WorkflowNode(None)
    child = WorkflowNode(None, parents = root)
    assert(child.parents == [root])
    child = WorkflowNode(None, parents = [root])
    assert(child.parents == [root])

def test_graph_size():
    root1, root2, child1, merge_child2, child3 = get_simple_fork_network()

    assert(root1.get_graph_size() == 1)
    assert(root2.get_graph_size() == 1)
    assert(child1.get_graph_size() == 2)
    assert(merge_child2.get_graph_size() == 4)
    assert(child3.get_graph_size() == 5)

def test_get_all_node():
    root1, root2, child1, merge_child2, child3 = get_simple_fork_network()

    assert(set([root1]) == set(root1.get_all_nodes()))
    assert(set([root2]) == set(root2.get_all_nodes()))
    assert(set([root2, child1]) == set(child1.get_all_nodes()))
    assert(set([root1, root2, child1, merge_child2]) == set(merge_child2.get_all_nodes()))
    assert(set([root1, root2, child1, merge_child2, child3]) == set(child3.get_all_nodes()))
