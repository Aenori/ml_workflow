
class SessionRecorder:
    def __init__(self, path):
        self.path = path

    def handle_data_source(self, original_function, args, kwargs):
        res = original_function(*args, **kwargs)

