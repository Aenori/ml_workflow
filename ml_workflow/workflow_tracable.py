import inspect
from . import execution_context
import re
import logging
from .misc_utils import TimeIt
logger = logging.getLogger(__name__)

class WorkflowTracable:
    AUTHORISED_ATTR = set(['name', 'highlight'])
    VALID_NAME_RE = re.compile("^[a-zA-Z0-9_\-\.]+$")

    def __init__(self, **kwargs):
        self.source_function = None

        if not (set(kwargs.keys()) <= self.get_authorized_attr()):
            unauthorised_keys = set(kwargs.keys()) - self.get_authorized_attr()
            raise Exception(
                f"Unauthorized keys for {self.__class__} :"
                f" {unauthorised_keys}")

        self.__dict__.update(kwargs)
        self.__check_name()

    def __call__(self, *args, **kwargs):
        if self.source_function is None:
            self.call_as_decorator(*args, **kwargs)
            return self

        with TimeIt() as t:
            res = self.call(*args, **kwargs)

        if hasattr(res, 'ml_workflow_node'):
            res.ml_workflow_node.add_stat('duration', t.duration())

            res.ml_workflow_node.add_logs(execution_context.ExecutionContext.flush_logs())

        return res

    def call(self, *args, **kwargs):
        with self:
            res = self.source_function(*args, **kwargs)

        return res

    def __str__(self):
        return self.name

    def __enter__(self):
        execution_context.notify_entry(self)

    def __exit__(self, type, value, traceback):
        execution_context.notify_exit(self)

    def call_as_decorator(self, *args, **kwargs):
        if ((len(args) != 1) or (len(kwargs) != 0)):
            logger.warning('First call of a Rule / DataSource should be as a decorator')    
        
        self.source_function = args[0]
        self.__doc__ = self.source_function.__doc__

    def get_source(self):
        if self.source_function is None:
            return ''
        return inspect.getsource(self.source_function)

    def get_authorized_attr(self):
        return self.__class__.AUTHORISED_ATTR

    def __check_name(self):
        if not WorkflowTracable.VALID_NAME_RE.match(self.name):
            raise Exception(f"Invalid name found : {self.name}. Only allowed characters are : a-zA-Z0-9_\-\.")
