from common_import import *

from ml_workflow.tracable_data_set import TracableDataFrame
from ml_workflow.context_utils import no_context_rule

@ml_workflow.rule
def set_is_old_from_age(df):
    df['IsOld'] = df['Age'] > 60

def test_tracable_data_set():
    df = TracableDataFrame({'Age' : [1, 67, 89, 10, 20]})

    df['Age'] += 1
    set_is_old_from_age(df)
    df['IsYoung'] =  df['Age'] < 20
    df['DansLaQuarantaine'] =  np.logical_and(df['Age'] >= 40, df['Age'] < 50)

    assert(set(df.columns) == set(['Age', 'IsYoung', 'IsOld', 'DansLaQuarantaine']))
    assert(df.ml_workflow_current_node.get_graph_size() == 4)
    
    assert(df.ml_workflow_current_node.origin is no_context_rule)
    assert(df.ml_workflow_current_node.modified_columns == set(['IsYoung', 'DansLaQuarantaine']))

    node = df.ml_workflow_current_node.get_previous_node()
    assert(node.origin is set_is_old_from_age)
    assert(node.modified_columns == set(['IsOld']))

    node = node.get_previous_node()
    assert(node.modified_columns == set(['Age']))

    node = node.get_previous_node()
    assert(node.get_previous_node() is None)

