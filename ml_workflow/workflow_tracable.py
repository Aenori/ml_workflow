import inspect
from . import execution_context
import re
import logging
from .misc_utils import TimeIt
from .decorator import Decorator

from packaging import version

logger = logging.getLogger(__name__)

class WorkflowTracable(Decorator):
    AUTHORISED_ATTR = set([
        'name', 'highlight', 'author', 'created_at',
        'version', 'branch', 'tags',
        'return_tuple', 
    ])
    VALID_NAME_RE = re.compile("^[a-zA-Z0-9_\-\.]+$")
    DEFAULT_VERSION = version.parse('0.0')

    def __init__(self, **kwargs):
        super().__init__()
        if not (set(kwargs.keys()) <= self.get_authorized_attr()):
            unauthorised_keys = set(kwargs.keys()) - self.get_authorized_attr()
            raise Exception(
                f"Unauthorized keys for {self.__class__} :"
                f" {unauthorised_keys}")

        # Default value
        self.set_default_values()

        self.__dict__.update(kwargs)
        if 'version' in kwargs:
            self.version = version.parse(kwargs['version'])
        self.__check_name()

    def set_default_values(self):
        self.return_tuple = False

    # This method is called by Decorator.__call__, after the first call,
    # as a decorator
    def call_as_decorated(self, *args, **kwargs):
        raise NotImplementedError()

    def call(self, *args, **kwargs):
        return self.source_function(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __enter__(self):
        execution_context.notify_entry(self)

    def __exit__(self, type, value, traceback):
        execution_context.notify_exit(self)

    def get_source(self):
        if self.source_function is None:
            return None
        return inspect.getsource(self.source_function)

    def get_branch(self):
        if not hasattr(self, 'branch'):
            return None
        return self.branch
    
    def get_tags(self):
        try:
            return self.tags
        except AttributeError:
            return None

    def get_version(self):
        if not self.has_version():
            return self.DEFAULT_VERSION
        return self.version

    def has_version(self):
        return hasattr(self, 'version')

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


