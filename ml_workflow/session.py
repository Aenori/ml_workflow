import random
import datetime as dt
import os, pathlib

from .session_recorder_player.session_recorder import SessionRecorder
from .session_recorder_player.session_record_player import SessionRecordPlayer

class SessionRecordContext:
    def __init__(self, recorder_player):
        self.recorder_player = recorder_player

    def __enter__(self):
        Session.active_recorder_player = self.recorder_player
        self.recorder_player.hook()

    def __exit__(self, type, value, traceback):
        Session.active_recorder_player = None
        self.recorder_player.unhook()

class Session:
    active_recorder_player = None

    @staticmethod
    def record_data_source(path = None, use_json = False, try_json = True):
        if path is None:
            now_as_file_compatible = dt.datetime.strftime(dt.datetime.now(), '%Y%m%d_%H%M%S')
            path = 'ml_workflow_frozen_session_{now_as_file_compatible}_{random.random.int(0,10000)}'

        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        Session.last_record = path

        return SessionRecordContext(SessionRecorder(path, use_json, try_json))

    @staticmethod
    def play_data_source_record(path = None):
        if path is None:
            path = Session.last_record
        assert(path)
        assert(os.path.isdir(path))

        return SessionRecordContext(SessionRecordPlayer(path))

