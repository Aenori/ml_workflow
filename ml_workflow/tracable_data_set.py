import pandas as pd
from .viz_utils import plot_model

from .workflow_node import WorkflowNode
from .workflow_node import get_user_code_origine_workflow

class TracableDataSetUtils:
    def plot_model(self, filename='temp_graph.png'):
        return plot_model(self.ml_workflow_node, filename)

    def get_workflow_origin(self):
        if self.ml_workflow_node is None:
            return None

        return self.ml_workflow_node.origin

    def set_workflow_origin(self, workflow_tracable, parents = None):
        if parents is None:
            parents = []

        self.ml_workflow_node = WorkflowNode(
            workflow_tracable,
            parents=parents
        )

    def set_default_ml_workflow_node_if_isnt_any(self):
        if self.ml_workflow_node is None:
            self.ml_workflow_node = get_user_code_origine_workflow()


pandas_class_to_wrapper = {}

def get_tracable_structure(klass):
    if klass not in pandas_class_to_wrapper:
        class TracableDataSetInstance(klass, TracableDataSetUtils):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.ml_workflow_node = None

        pandas_class_to_wrapper[klass] = TracableDataSetInstance

    return pandas_class_to_wrapper[klass]

TracableDataFrame = get_tracable_structure(pd.DataFrame)

class TracableList(list):
    def set_workflow_origin(self, workflow_tracable, parents = None):
        if parents is None:
            parents = []

        self.ml_workflow_node = WorkflowNode(
            workflow_tracable,
            parents=parents
        )    

    def __eq__(self, other):
        return super().__eq__(other)

def get_tracable_data_set(data_set):
    if isinstance(data_set, pd.DataFrame):
        return TracableDataFrame(data_set)
    if isinstance(data_set, list):
        return TracableList(data_set)
    raise Exception(f'Unknown source type {type(data_set)}')
