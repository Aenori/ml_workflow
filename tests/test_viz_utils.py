from common_import import *

from ml_workflow.viz_utils import check_pydot, model_to_dot, plot_model
from tests.utils.compare_or_generate_ref import compare_or_generate_ref

def get_simple_graph_with_fork():
    root1 = WorkflowNode('DataSource1')
    root2 = WorkflowNode('DataSource2')

    child1 = WorkflowNode('Processing_on_DS2', parents = root2)
    merge_child2 = WorkflowNode('Merge_sources', parents = [root1, child1])
    leaf_node = WorkflowNode('LeafNode', parents = merge_child2)

    return leaf_node

def test_check_pydot():
    assert(check_pydot())

def test_model_to_dot():
    leaf_node = get_simple_graph_with_fork()
    model_as_dot = model_to_dot(leaf_node)

    model_as_dot.write('test_regression.dot', format='dot')

def test_plot_model_as_svg():
    WorkflowNode.next_id = 1
    _test_plot_model('test_regression.svg')

def test_plot_model_as_png():
    _test_plot_model('test_regression.png')

def _test_plot_model(filename):
    leaf_node = get_simple_graph_with_fork()
    plot_model(leaf_node, filename)

    compare_or_generate_ref(filename)