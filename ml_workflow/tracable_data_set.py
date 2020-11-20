import pandas as pd
from . import viz_utils

from .workflow_node import WorkflowNode
from .workflow_node import get_user_code_origine_workflow

class TracableDataSetUtils:
    # This act as a default value for all TracableDataFrame or other objects
    # Just note that when you write
    #   df.ml_workflow_node = something
    # With df being an instance of TracableDataFrame, you are not modifying 
    # this variable, but creating an instance level one that shadows it
    ml_workflow_node = None

    def plot_model(self, filename='temp_graph.svg'):
        return viz_utils.plot_model(
            self.ml_workflow_node, 
            filename
        )

    def plot_model_full_detail(self, directory=None, ts=None):
        return viz_utils.plot_model_full_detail(
            self.ml_workflow_node, 
            directory=directory, 
            ts=ts
        )

    def get_workflow_origin(self):
        if self.ml_workflow_node is None:
            return None

        return self.ml_workflow_node.origin

    def set_workflow_origin(self, workflow_tracable, previous = None):
        if previous is None:
            previous = []

        self.ml_workflow_node = WorkflowNode(
            workflow_tracable,
            previous=previous
        )

    def set_default_ml_workflow_node_if_isnt_any(self):
        if self.ml_workflow_node is None:
            self.ml_workflow_node = get_user_code_origine_workflow()

pandas_class_to_wrapper = {}

def get_tracable_structure(klass):
    if klass in pandas_class_to_wrapper:
        return pandas_class_to_wrapper[klass]
    return klass

class TracableDataFrame(pd.DataFrame, TracableDataSetUtils): pass

pandas_class_to_wrapper[pd.DataFrame] = TracableDataFrame

class TracableList(list):
    def set_workflow_origin(self, workflow_tracable, previous = None):
        if previous is None:
            previous = []

        self.ml_workflow_node = WorkflowNode(
            workflow_tracable,
            previous=previous
        )

    def __eq__(self, other):
        return super().__eq__(other)

def get_tracable_data_set(data_set):
    if isinstance(data_set, pd.DataFrame):
        return TracableDataFrame(data_set)
    if isinstance(data_set, list):
        return TracableList(data_set)

    msg = f"""ML_WORKFLOW : ERROR
get_tracable_data_set has received an object of type {type(data_set)}
The more probable cause is that you set @DataSource on a function that 
returns something else that supported types : [pd.DataFrame, list]
"""

    raise Exception(msg)
