import pandas as pd

from . import execution_context
from . import dataframe_tracker


class TracableDataFrame(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        self.ml_workflow_current_node = None
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        dataframe_tracker.handle_change(self, key)
        super().__setitem__(*args, **kwargs)

def get_tracable_data_set(data_source):
    if isinstance(data_source, pd.DataFrame):
        return TracableDataFrame(data_source)
