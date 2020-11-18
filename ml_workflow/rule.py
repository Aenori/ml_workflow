from .workflow_tracable import WorkflowTracable
import collections

class Rule(WorkflowTracable):
    rule_by_name = collections.defaultdict(list)
    reference_name_to_rule = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Rule.rule_by_name[self.name].append(self)

    @classmethod
    def call_from_reference_name(cls, reference_name):
        if reference_name not in cls.reference_name_to_rule:
            v = lambda rule : rule.__dict__.get('version', '')
            best_rule = None
            best_rule_version = None

            for rule in cls.rule_by_name[reference_name]:
                if not hasattr(rule, 'author'):
                    if (best_rule is None) or (v(rule) > v(best_rule)):
                        best_rule = rule
            
            cls.reference_name_to_rule[reference_name] = best_rule

        return cls.reference_name_to_rule[reference_name]

    @classmethod
    def set_for_reference_name(cls, reference_name, rule):
        cls.reference_name_to_rule[reference_name] = rule

