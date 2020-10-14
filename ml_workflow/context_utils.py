from . import execution_context
from .rule import Rule

no_context_rule = Rule(source_function=None, name='Unspecified rule')
not_a_rule_context = Rule(source_function=None, name='not_a_rule_context')


def get_current_rule():
    current = execution_context.get_current_context()

    if current is None:
        return no_context_rule
    if not isinstance(current, Rule):
        return not_a_rule_context

    return current
