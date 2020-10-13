from ml_workflow.data_source import DataSource

import pickle
from .abstract_session_recorder_player import AbstractSessionRecorderPlayer


class SessionRecordPlayer(AbstractSessionRecorderPlayer):
    def __init__(self, path):
        super().__init__(path)
        self.load_data()

    def load_data(self):
        with open(f'{self.path}/single_pickle_storage', 'rb') as f:
            self.args_recorded_list, self.res_recorded_list = pickle.load(f)

    def handle_data_source(self, data_source, *args, **kwargs):
        assert(self.active)
        args_recorded = self.clean_args(data_source, args, kwargs)
        result_recorded = self.find_recorded_result(data_source, args_recorded)

        if result_recorded is None:
            raise Exception(
                f"For data source {data_source.name}, could not find args {args_recorded}")

        return result_recorded
