import random
import datetime as dt

from .session_recorder_player.session_recorder import SessionRecorder
from .session_recorder_player.session_record_player import SessionRecordPlayer

class SessionRecordPlayerContext:
    def __init__(self, recorder_player):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

class Session:
    active_recorder_player = None

    @staticmethod
    def has_active_recorder_player():
        return Session.active_recorder_player is not None

    @staticmethod
    def handle_data_source(source_function, args, kwargs):
        return Session.active_recorder_player.handle_data_source(source_function, args, kwargs)

    @staticmethod
    def record_data_source(path = None):
        if path is None:
            now_as_file_compatible = dt.datetime.strftime(dt.datetime.now(), '%Y%m%d_%H%M%S')
            path = 'ml_workflow_frozen_session_{now_as_file_compatible}_{random.random.int(0,10000)}'
        
        os.mkdir(path)
        Session.last_record = path

        return SessionRecordContext(self, SessionRecorder(path))

    @staticmethod
    def play_data_source_record(path = None):
        if path is None:
            path = Session.last_record
        assert(path)
        assert(os.path.isdir(path))

        return SessionRecordContext(self, SessionRecordPlayer(path))
        

