import inspect
from . import execution_context

import logging
logger = logging.getLogger(__name__)

class WorkflowTracable:
    AUTHORISED_ATTR = set(['name', 'highlight'])

    def __init__(self, **kwargs):
        self.source_function = None

        if not (set(kwargs.keys()) <= self.get_authorized_attr()):
            unauthorised_keys = set(kwargs.keys()) - self.get_authorized_attr()
            raise Exception(
                f"Unauthorized keys for {self.__class__} :"
                " {unauthorised_keys}")

        self.__dict__.update(kwargs)

    def __call__(self, *args, **kwargs):
        if self.source_function is None:
            self.call_as_decorator(*args, **kwargs)
            return self

        return self.call(*args, **kwargs)

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

    def get_source(self):
        return inspect.getsource(self.source_function)

    def get_authorized_attr(self):
        return self.__class__.AUTHORISED_ATTR
