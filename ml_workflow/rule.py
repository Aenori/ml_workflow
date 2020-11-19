from .workflow_tracable import WorkflowTracable
import collections
from . import rule_reference
from . import rule_config_manager

class Rule(WorkflowTracable):
    rule_by_name = collections.defaultdict(list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Rule.rule_by_name[self.name].append(self)
        rule_config_manager.RuleConfigManager.clean_reference_for(self.name)

    # Override Decorator.call_as_decorator
    def call_as_decorator(self, *args, **kwargs):
        super().call_as_decorator(*args, **kwargs)

        this_rule_reference = rule_reference.RuleReference.dict_by_name.get(self.name)
        if this_rule_reference:
            this_rule_reference.check_coherence(self)

    @classmethod
    def set_for_reference_name(_, name, rule):
        rule_config_manager.RuleConfigManager.set_for_reference_name(name, rule)

    @classmethod
    def get_from_reference_name(cls, name):
        return rule_config_manager.RuleConfigManager.get_from_reference_name(name)
