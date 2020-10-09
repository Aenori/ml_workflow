import pandas as pd

from . import execution_context

class TracableDataFrame(pd.DataFrame):
    def __init__(self, original_df):
        super().__init__(original_df)

    def __setitem__(self, key, value):
        self.handle_change(key)
        super().__setitem__(*args, **kwargs)

    # not part of the API
    def get_current_node(self):
        pass

    def handle_change(self, key):
        pass

def get_tracable_data_set(data_source):
    if isinstance(data_source, pd.DataFrame):
        return TracableDataFrame(data_source)
