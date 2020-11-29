import logging
logger = logging.getLogger(__name__)
import os

class Decorator:
    def __init__(self):
        self.source_function = None

    def __call__(self, *args, **kwargs):
        with self:
            if self.source_function is None:
                self.call_as_decorator(*args, **kwargs)
                return self

            return self.call_as_decorated(*args, **kwargs)

    def call_as_decorator(self, *args, **kwargs):
        if ((len(args) != 1) or (len(kwargs) != 0)):
            logger.warning(f'First call of a {self.__class__.__name__} should be as a decorator')    
        
        self.source_function = args[0]
        self.__doc__ = self.source_function.__doc__

    def get_source_function_args(self):
        return self.source_function.__code__.co_varnames

    def get_definition_location(self):
        f = self.source_function
        res = f"{f.__globals__['__file__']}:{f.__code__.co_firstlineno}"
        if res.startswith(os.getcwd()):
            res = res.replace(os.getcwd(), '')

        return res

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass
        