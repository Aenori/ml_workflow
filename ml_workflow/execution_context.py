import collections
import threading
import logging

logger = logging.getLogger(__name__)

class ExecutionContext:
    log_stream = []
    context_by_thread = collections.defaultdict(list)

    @classmethod
    def log(cls, log_message):
        cls.log_stream.append(log_message)

    @classmethod
    def flush_logs(cls):
        res = cls.log_stream
        cls.log_stream = []

        return res

def notify_entry(workflow_tracable):
    ExecutionContext.context_by_thread[threading.get_ident()].append(workflow_tracable)

def notify_exit(workflow_tracable):
    assert(ExecutionContext.context_by_thread[threading.get_ident()][-1] is workflow_tracable)
    ExecutionContext.context_by_thread[threading.get_ident()].pop()

def get_current_full_context():
    return tuple(ExecutionContext.context_by_thread[threading.get_ident()])

# Not used at the moment
# def get_current_last_context():
#     context = ExecutionContext.context_by_thread[threading.get_ident()]
#     if len(context):
#         return context[-1]
#     return None
