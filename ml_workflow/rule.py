import pandas as pd

from .workflow_tracable import WorkflowTracable


class Rule(WorkflowTracable):
    AUTHORISED_ATTR = WorkflowTracable.AUTHORISED_ATTR.union(
        set(['constraints'])
    )

    rule_by_name = {}
    reference_name_to_rule = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Rule.rule_by_name[self.name] = self

    @classmethod
    def call_from_reference_name(cls, reference_name):
        if reference_name in cls.reference_name_to_rule:
            return cls.reference_name_to_rule[reference_name]
        else:
            return cls.rule_by_name[reference_name]

    @classmethod
    def set_for_reference_name(cls, reference_name, rule):
        cls.reference_name_to_rule[reference_name] = rule

    @classmethod
    def unset_for_reference_name(cls, reference_name):
        if reference_name in cls.reference_name_to_rule:
            del cls.reference_name_to_rule[reference_name]

