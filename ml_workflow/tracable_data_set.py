import pandas as pd

from . import execution_context
from . import dataframe_tracker

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
            res = get_tracable_structure(orig_res.__class__)(orig_res)
            dataframe_tracker.handle_selection(self, key, res)

            return res

    pandas_class_to_wrapper[klass] = TracableClass

    return TracableClass

TracableDataFrame = get_tracable_structure(pd.DataFrame)

def get_tracable_data_set(data_source):
    if isinstance(data_source, pd.DataFrame):
        return TracableDataFrame(data_source)

    raise Exception('Unknown source type')
