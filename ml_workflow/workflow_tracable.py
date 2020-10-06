
class WorkflowTracable:
    AUTHORISED_ATTR = set(['name'])    
    
    def __init__(self, source_function, **kwargs):
        self.source_function = source_function
        
        assert(set(kwargs.keys()) <= WorkflowTracable.AUTHORISED_ATTR)
        self.__dict__.update(kwargs)
        
        if not 'name' in kwargs:
            self.name = source_function.__name__
            
    def __call__(self, *args, **kwargs):
        print(f"I have been called with args : {args}, {kwargs}")
        return self.source_function(*args, **kwargs)
    
    def get_source(self):
        return inspect.getsource(self.source_function)
        