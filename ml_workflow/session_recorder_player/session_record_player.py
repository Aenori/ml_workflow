from ml_workflow.data_source import DataSource

import pickle
import json
import pandas as pd

from .abstract_session_recorder_player import AbstractSessionRecorderPlayer


class SessionRecordPlayer(AbstractSessionRecorderPlayer):
    def __init__(self, path):
        super().__init__(path)
        self.load_data()

    def load_data(self):
        with open(f'{self.path}/{self.master_json_filename}', 'r') as f:
            master_json = json.load(f)

        for ds, records in master_json.items():
            args_recorded_list_for_ds = self.args_recorded_list[ds]
            res_recorded_list_for_ds = self.res_recorded_list[ds]

            for arg, record in records:
                args_recorded_list_for_ds.append((tuple(arg[0]), arg[1]))

                if isinstance(record, str) and record.startswith('MLWF_File : '):
                    res_recorded_list_for_ds.append(self.load_from_file_tag(record))
                else:
                    res_recorded_list_for_ds.append(record)

            # print((ds, len(self.args_recorded_list[ds]), len(self.res_recorded_list[ds])))

    def load_from_file_tag(self, record):
        filename = record[len(self.file_tag):]

        if filename.endswith('.csv.gz') or filename.endswith('.csv'):
            return pd.read_csv(filename)
        elif filename.endswith('.pickle'):
            with open(filename, 'rb') as f:
                return pickle.load(f)
        else:
            with open(filename, 'r') as f:
                return json.load(f)

    def handle_data_source(self, data_source, *args, **kwargs):
        assert(self.active)
        args_recorded = self.clean_args(data_source, args, kwargs)
        result_recorded = self.find_recorded_result(data_source, args_recorded)

        if result_recorded is None:
            raise Exception(
                f"For data source {data_source.name},"
                f"Recorded list : {self.args_recorded_list[data_source.get_qual_name()]}"
                f" could not find args {args_recorded}")

        return result_recorded
