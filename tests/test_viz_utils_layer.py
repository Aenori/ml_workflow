import python_path

from ml_workflow.workflow_node import WorkflowNode
from ml_workflow import viz_utils_layer 

import pydot

def test_pydot_behaviour():
    dot = pydot.Dot()

    node1 = pydot.Node('node1') 
    dot.add_node(node1)
    assert([n.get_name() for n in dot.get_node('node1')] == [node1.get_name()])

    cluster = pydot.Cluster(style='dashed', graph_name='sub_graph')
    node2 = pydot.Node('node2')
    cluster.add_node(node2)
    dot.add_subgraph(cluster)

    assert(dot.get_node('node2') == [])

def test_graph_conversion_1():
    node_initial = WorkflowNode(['Source'])
    node1 = WorkflowNode(['Rule1'], previous = node_initial)
    node2 = WorkflowNode(['Rule1', 'Rule2'], previous = node1)
    node3 = WorkflowNode(['Rule1'], previous = node2)
    node4 = WorkflowNode(['Rule1', 'Rule2', 'Rule3'], previous = node3)
    node5 = WorkflowNode(['Rule1', 'Rule2', 'Rule4'], previous = node4)

    layer = viz_utils_layer.convert_node_to_layer(node5)

    assert(len(layer.previous_layers) == 1)
    assert(layer.previous_layers[0].layer_origin == 'Source')
    assert(len(layer.previous_layers[0].previous_layers) == 0)
    assert(len(layer.sub_layers) == 1)
    assert(len(layer.sub_layers[0].sub_layers) == 2)

    assert((len(layer.get_all_nodes()) + len(layer.get_duplicated_id())) == len(node5.get_all_nodes()))
    assert(set(layer.get_all_included_node_id()) == set(node.id for node in node5.get_all_nodes()))
