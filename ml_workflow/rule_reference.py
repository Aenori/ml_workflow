from .decorator import Decorator
from . import rule

class RuleReference(Decorator):
    dict_by_name = {}

    def __init__(self, name):
        self.name = name
        RuleReference.dict_by_name[self.name] = self
        super().__init__()

    # Override Decorator.call_as_decorator
    def call_as_decorator(self, *args, **kwargs):
        super().call_as_decorator(*args, **kwargs)
        for i_rule in rule.Rule.rule_by_name[self.name]:
            self.check_coherence(i_rule)

    def call_as_decorated(self, *args, **kwargs):
        return rule.Rule.get_from_reference_name(self.name)(*args, **kwargs)

    def check_coherence(self, rule_):
        if self.get_source_function_args() != rule_.get_source_function_args():
            msg = f"ERROR : found incoherence between reference and rule for :\n"
            msg += f"  {rule_}\n"
            msg += f"  Args list doesn't match :\n"
            msg += f"  {self.get_source_function_args()} != {rule_.get_source_function_args()}\n"
            msg += f"  rule defined in {rule_.get_definition_location()}\n"
            msg += f"  rule reference defined in {self.get_definition_location()}\n"

            raise Exception(msg)

