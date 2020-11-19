from .workflow_tracable import WorkflowTracable
import collections
from . import rule_reference

class Rule(WorkflowTracable):
    rule_by_name = collections.defaultdict(list)
    reference_name_to_rule = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Rule.rule_by_name[self.name].append(self)

    # Override Decorator.call_as_decorator
    def call_as_decorator(self, *args, **kwargs):
        super().call_as_decorator(*args, **kwargs)

        this_rule_reference = rule_reference.RuleReference.dict_by_name.get(self.name)
        if this_rule_reference:
            this_rule_reference.check_coherence(self)

    @classmethod
    def get_from_reference_name(cls, reference_name):
        if reference_name not in cls.reference_name_to_rule:
            v = lambda rule : rule.__dict__.get('version', '')
            best_rule = None

            for rule in cls.rule_by_name[reference_name]:
                if not hasattr(rule, 'branch'):
                    if (best_rule is None) or (v(rule) > v(best_rule)):
                        best_rule = rule
            
            cls.reference_name_to_rule[reference_name] = best_rule

        return cls.reference_name_to_rule[reference_name]

    @classmethod
    def set_for_reference_name(cls, reference_name, rule):
        cls.reference_name_to_rule[reference_name] = rule
