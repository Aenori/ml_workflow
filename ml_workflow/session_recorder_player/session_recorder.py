from collections import defaultdict
import pickle

from .abstract_session_recorder_player import AbstractSessionRecorderPlayer

class SessionRecorder(AbstractSessionRecorderPlayer):
    def __init__(self, path, use_json, try_json):
        super().__init__(path)
        self.args_recorded_list = defaultdict(list)
        self.res_recorded_list = defaultdict(list)

    def unhook(self):
        super().unhook()
        self.save()

    def save(self):
        with open(f'{self.path}/single_pickle_storage', 'wb') as f:
            pickle.dump((self.args_recorded_list, self.res_recorded_list), file = f)

    def handle_data_source(self, data_source, *args, **kwargs):
        assert(self.active)
        res = self.unhooked_call(data_source, *args, **kwargs)

        args_recorded = self.clean_args(data_source, args, kwargs)

        known_record = self.find_recorded_result(data_source, args_recorded)
        if known_record:
            if res != known_record:
                raise Exception(f"Cannot record result, two differents results received from {data_source.name}")
        else:
            ds_recorded_args = self.args_recorded_list[data_source.get_qual_name()]
            ds_recorded_res = self.res_recorded_list[data_source.get_qual_name()]

            ds_recorded_args.append(args_recorded)
            ds_recorded_res.append(res)

        return res