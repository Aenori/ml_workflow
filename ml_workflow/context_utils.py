from . import execution_context
from . import rule

def get_current_context():
    current = execution_context.get_current_full_context()

    if len(current) == 0:
        return (rule.no_context_rule,)

    return tuple(current)
