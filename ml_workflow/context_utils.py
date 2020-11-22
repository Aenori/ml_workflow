from . import execution_context
from .rule import Rule

no_context_rule = Rule(name='Unspecified_rule')
not_a_rule_context = Rule(name='not_a_rule_context')


def get_current_context():
    current = execution_context.get_current_full_context()

    if len(current) == 0:
        return (no_context_rule,)

    return tuple(current)
