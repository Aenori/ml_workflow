import inspect
from . import execution_context
import re
import logging
from .misc_utils import TimeIt
from .decorator import Decorator

from packaging import version

logger = logging.getLogger(__name__)

class WorkflowTracable(Decorator):
    AUTHORISED_ATTR = set(['name', 'highlight', 'version', 'branch', 'tags'])
    VALID_NAME_RE = re.compile("^[a-zA-Z0-9_\-\.]+$")

    def __init__(self, **kwargs):
        super().__init__()
        if not (set(kwargs.keys()) <= self.get_authorized_attr()):
            unauthorised_keys = set(kwargs.keys()) - self.get_authorized_attr()
            raise Exception(
                f"Unauthorized keys for {self.__class__} :"
                f" {unauthorised_keys}")

        self.__dict__.update(kwargs)
        if 'version' in kwargs:
            self.version = version.parse(kwargs['version'])
        self.__check_name()

    # This method is called by Decorator.__call__, after the first call,
    # as a decorator
    def call_as_decorated(self, *args, **kwargs):
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

    def get_source(self):
        if self.source_function is None:
            return ''
        return inspect.getsource(self.source_function)

    def get_branch(self):
        if not hasattr(self, 'branch'):
            return None
        return self.branch
    
    def get_version(self):
        if not hasattr(self, 'version'):
            return None
        return self.version

    @classmethod
    def get_authorized_attr(cls):
        return cls.AUTHORISED_ATTR

    def get_full_details(self):
        msg = f"Rule :\n"
        for k in self.get_authorized_attr():
            if hasattr(self, k):
                msg += f"  {k} => {getattr(self, k)}\n"
        msg += f"  origin : {self.get_definition_location()}"
        
        return msg

    def __check_name(self):
        if not WorkflowTracable.VALID_NAME_RE.match(self.name):
            raise Exception(f"Invalid name found : {self.name}. Only allowed characters are : a-zA-Z0-9_\-\.")


