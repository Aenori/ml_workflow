from ml_workflow.data_source import DataSource

import pickle
from . import utils

class SessionRecordPlayer:
    def __init__(self, path):
        self.path = path

        with open(f'{self.path}/single_pickle_storage', 'rb') as f:
            self.args_recorded_list, self.res_recorded_list = pickle.load(f)
        
    def hook(self):
        DataSource.__original_call = DataSource.call
        DataSource.call = lambda *args, **kwargs : self.handle_data_source(*args, **kwargs)

    def unhook(self):
        DataSource.call = DataSource.__original_call
        del DataSource.__original_call

    def handle_data_source(self, data_source, *args, **kwargs):        
        ds_recorded_args = self.args_recorded_list[data_source.get_qual_name()]
        ds_recorded_res = self.res_recorded_list[data_source.get_qual_name()] 

        args_recorded = utils.clean_args(data_source, args, kwargs)

        if args_recorded not in ds_recorded_args:
            raise Exception(f"For data source {data_source.name}, could not find args {args_recorded}") 
        
        return ds_recorded_res[ds_recorded_args.index(args_recorded)]
