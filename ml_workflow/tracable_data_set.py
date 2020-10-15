import pandas as pd

from . import execution_context
from . import dataframe_tracker

from .workflow_node import WorkflowNode
pandas_class_to_wrapper = {}

# Should be migrated to using metaclass


def get_tracable_structure(klass):
    if klass in pandas_class_to_wrapper:
        return pandas_class_to_wrapper[klass]

    class TracableClass(klass):
        def __init__(self, *args, **kwargs):
            # Here we are assuming that no pandas object is making deep copy
            # when passed its own type
            super().__init__(*args, **kwargs)
            self.ml_workflow_current_node = None

        def __setitem__(self, key, value):
            dataframe_tracker.handle_change(self, key)
            return super().__setitem__(key, value)

        def __getitem__(self, key):
            orig_res = super().__getitem__(key)
            return self.__handle_new_df_return(orig_res, parents=[self], key=key)

        def merge(self, right, *args, **kwargs):
            orig_res = super().merge(right, *args, **kwargs)
            return self.__handle_new_df_return(orig_res, parents=[self, right])
        
        def __handle_new_df_return(self, orig_res, parents, key=None):
            res = get_tracable_structure(orig_res.__class__)(orig_res)
            dataframe_tracker.handle_selection(self, res, parents, key)

            return res

        def plot_model(self, filename='temp_graph.png'):
            from .viz_utils import plot_model
            return plot_model(self.ml_workflow_current_node, filename)

        def set_workflow_origin(self, workflow_tracable, parents = None):
            if parents is None:
                parents = []

            self.ml_workflow_current_node = WorkflowNode(
                workflow_tracable,
                parents=parents
            )

    pandas_class_to_wrapper[klass] = TracableClass

    return TracableClass


TracableDataFrame = get_tracable_structure(pd.DataFrame)

class TracableList(list):
    def set_workflow_origin(self, workflow_tracable, parents = None):
        if parents is None:
            parents = []

        self.ml_workflow_current_node = WorkflowNode(
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
    raise Exception('Unknown source type')
