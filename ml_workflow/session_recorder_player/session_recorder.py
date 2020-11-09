from collections import defaultdict
import pickle
import json
import os

import pandas as pd

from .abstract_session_recorder_player import AbstractSessionRecorderPlayer
from ..app_config import app_config

class SessionRecorder(AbstractSessionRecorderPlayer):
    def __init__(self, path, use_json, try_json):
        super().__init__(path)

    def unhook(self):
        super().unhook()
        self.save()

    def save(self):
        master_json = {}
        for data_source, v_list in self.args_recorded_list.items():
            record_for_datasource = []
            res_recorded = self.res_recorded_list[data_source]
            for i, (arg, res) in enumerate(zip(v_list, res_recorded)):
                record_for_datasource.append([arg, self.handle_recording(data_source, i, res)])

            master_json[data_source] = record_for_datasource

        self.json_dumps(f'{self.path}/{self.master_json_filename}', master_json)

    def json_dumps(_, filename, data):
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4, sort_keys=True))

    def file_with_tag(self, filename):
        return f"{self.file_tag}{filename}"

    def handle_recording(self, data_source, i, res):
        if isinstance(res, (pd.DataFrame, list, dict)):
            filename_without_extension = os.path.join(self.path, f'{data_source}_{i}')

            # If res is a dataframe, saving it in a different file as csv
            if isinstance(res, pd.DataFrame):
                filename = filename_without_extension + '.h5'
                res.to_hdf(filename)
                return self.file_with_tag(filename)
            else:
                # res is a list or dict, saving it as json.
                filename = filename_without_extension + '.json'
                self.json_dumps(filename, res)
                return self.file_with_tag(filename)
        else:
            # Simple type, just save it directly in the master.json
            return res


    def handle_data_source(self, data_source, *args, **kwargs):
        assert(self.active)
        res = self.unhooked_call(data_source, *args, **kwargs)

        args_recorded = self.clean_args(data_source, args, kwargs)

        known_record = self.find_recorded_result(data_source, args_recorded)
        if known_record:
            if res != known_record:
                raise Exception(f"Cannot record result, two differents"
                                "results received from {data_source.name}")
        else:
            ds_qual_name = data_source.get_qual_name()

            ds_recorded_args = self.args_recorded_list[ds_qual_name]
            ds_recorded_res = self.res_recorded_list[ds_qual_name]

            ds_recorded_args.append(args_recorded)
            ds_recorded_res.append(res)

        return res
