from ml_workflow.data_source import DataSource

class AbstractSessionRecorderPlayer:
    def __init__(self, path):
        self.active = False
        self.path = path

    @staticmethod
    def unhooked_call(data_source, *args, **kwargs):
        return data_source.__original_call(*args, **kwargs)

    @staticmethod
    def clean_args(data_source, args, kwargs):
        args = list(args)
        for index in data_source.frozen_ignore_args_positions:
            if index < len(args):
                del args[index]
        args = tuple(args)

        for key in data_source.frozen_ignore_args:
            if key in kwargs:
                del kwargs[key]

        return args, kwargs

    def hook(self):
        DataSource.__original_call = DataSource.call
        this = self

        def hooked_call(*args, **kwargs):
            assert(this.active)
            return this.handle_data_source(*args, **kwargs)

        DataSource.call = hooked_call
        self.active = True

    def unhook(self):
        DataSource.call = DataSource.__original_call
        del DataSource.__original_call
        self.active = False

    def find_recorded_result(self, data_source, args_recorded):
        ds_recorded_args = self.args_recorded_list[data_source.get_qual_name()]
        ds_recorded_res = self.res_recorded_list[data_source.get_qual_name()]

        if args_recorded not in ds_recorded_args:
            return None

        return ds_recorded_res[ds_recorded_args.index(args_recorded)]

