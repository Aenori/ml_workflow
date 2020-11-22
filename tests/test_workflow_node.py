import python_path

from ml_workflow.workflow_node import WorkflowNode

def test_match_origins():
    wf1 = WorkflowNode(origin=('A', 'B'))

    assert(wf1.match_origin(('A', 'B')))
    assert(wf1.match_origin(('A',)))
    assert(not wf1.match_origin(('A', 'C')))

def test_origin_immutable():
    origin = [1, 2, 3]
    wf1 = WorkflowNode(origin=origin)
    origin.pop()
    assert(len(wf1.origin) == 3)
