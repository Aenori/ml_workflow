from ml_workflow import DataSource

class SessionRecorder:
    def __init__(self, path):
        self.path = path

    def hook(self):
        DataSource.__original_call = DataSource.call
        DataSource.call = lambda *args, **kwargs : self.handle_data_source(*args, **kwargs)

    def unhook(self):
        DataSource.call = DataSource.__original_call
        del DataSource.__original_call

    def handle_data_source(self, data_source, *args, **kwargs):
        print(data_source.name)

        return data_source.__original_call(*args, **kwargs)

