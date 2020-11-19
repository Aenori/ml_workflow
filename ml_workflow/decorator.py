
class Decorator:
    def __init__(self):
        self.source_function = None

    def __call__(self, *args, **kwargs):
        if self.source_function is None:
            self.call_as_decorator(*args, **kwargs)
            return self

        return self.call_as_decorated(*args, **kwargs)

    def call_as_decorator(self, *args, **kwargs):
        if ((len(args) != 1) or (len(kwargs) != 0)):
            logger.warning(f'First call of a {self.__class__.__name__} should be as a decorator')    
        
        self.source_function = args[0]
        self.__doc__ = self.source_function.__doc__
        