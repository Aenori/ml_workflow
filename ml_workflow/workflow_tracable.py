import inspect
from . import execution_context

class WorkflowTracable:
    AUTHORISED_ATTR = set(['name'])    
    
    def __init__(self, source_function = None, **kwargs):
        self.source_function = source_function
        
        if not (set(kwargs.keys()) <= self.get_authorized_attr()):
            unauthorised_keys = set(kwargs.keys()) - self.get_authorized_attr()
            raise Exception(f"Unauthorized keys for {self.__class__} : {unauthorised_keys}")

        self.__dict__.update(kwargs)
        
        if not 'name' in kwargs:
            self.name = source_function.__name__
            
    def __call__(self, *args, **kwargs):
        with self:
            res = self.source_function(*args, **kwargs)
        
        return res

    def __enter__(self):
        execution_context.notify_entry(self)

    def __exit__(self, type, value, traceback):
        execution_context.notify_exit(self)

    def get_source(self):
        return inspect.getsource(self.source_function)
        
    def get_authorized_attr(self):
        return self.__class__.AUTHORISED_ATTR

class WorkflowTracableDecorator:
    def __init__(self, klass):
        self.klass = klass

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            return lambda f : self(f, **kwargs)
        assert(len(args) == 1)
        
        return self.klass(*args, **kwargs)