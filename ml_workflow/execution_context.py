import collections
import threading
import logging

logger = logging.getLogger(__name__)

context_by_thread = collections.defaultdict(list)

class ExecutionContext:
    log_stream = []

    @classmethod
    def log(cls, log_message):
        cls.log_stream.append(log_message)

    @classmethod
    def flush_logs(cls):
        res = cls.log_stream
        cls.log_stream = []

        return res

def notify_entry(workflow_tracable):
    context_by_thread[threading.get_ident()].append(workflow_tracable)


def notify_exit(workflow_tracable):
    assert(context_by_thread[threading.get_ident()][-1] is workflow_tracable)
    context_by_thread[threading.get_ident()].pop()


def get_current_context():
    context = context_by_thread[threading.get_ident()]
    if len(context):
        return context[-1]
    return None
