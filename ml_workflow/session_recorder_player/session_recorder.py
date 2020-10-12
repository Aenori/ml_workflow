from ml_workflow.data_source import DataSource

from collections import defaultdict
import pickle

from . import utils

class SessionRecorder:
    def __init__(self, path, use_json, try_json):
        self.__dict__.update(locals())
        self.args_recorded_list = defaultdict(list)
        self.res_recorded_list = defaultdict(list)

    def hook(self):
        DataSource.__original_call = DataSource.call
        DataSource.call = lambda *args, **kwargs : self.handle_data_source(*args, **kwargs)

    def unhook(self):
        DataSource.call = DataSource.__original_call
        del DataSource.__original_call

        with open(f'{self.path}/single_pickle_storage', 'wb') as f:
            pickle.dump((self.args_recorded_list, self.res_recorded_list), file = f)

    def handle_data_source(self, data_source, *args, **kwargs):
        res = data_source.__original_call(*args, **kwargs)
        
        args_recorded = utils.clean_args(data_source, args, kwargs)

        ds_recorded_args = self.args_recorded_list[data_source.get_qual_name()]
        ds_recorded_res = self.res_recorded_list[data_source.get_qual_name()] 

        if args_recorded in ds_recorded_args:
            registered_res = ds_recorded_res[ds_recorded_args.index(args_recorded)]

            if res != registered_res:
                raise Exception(f"Cannot record result, two differents results received from {data_source.name}")
        else:
            ds_recorded_args.append(args_recorded)
            ds_recorded_res.append(res)         

        return res
