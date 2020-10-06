from .workflow_tracable import WorkflowTracable

def ml_rule(*args, **kwargs):
    if len(args) == 0:
        return lambda f : ml_rule(f, **kwargs)
    assert(len(args) == 1)
    
    return Rule(*args, **kwargs)
    
class Rule(WorkflowTracable):
    pass