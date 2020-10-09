import pandas as pd

from . import execution_context

class TracableDataFrame(pd.DataFrame):
    def __init__(self, original_df):
        super().__init__(original_df)

    def __setitem__(self, *args, **kwargs):

        super().__setitem__(*args, **kwargs)

def get_tracable_data_set(data_source):
    if isinstance(data_source, pd.DataFrame):
        return TracableDataFrame(data_source)
