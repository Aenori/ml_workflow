from .workflow_tracable import WorkflowTracable, WorkflowTracableDecorator


class Rule(WorkflowTracable):
    rule_by_name = {}
    reference_name_to_rule = {}

    def __init__(self, source_function=None, **kwargs):
        super().__init__(source_function, **kwargs)
        Rule.rule_by_name[self.name] = self

    def get_name(self):
        try:
            return self.name
        except AttributeError:
            assert(self.source_function is not None)
            self.name = self.source_function.__name__

            return self.name

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


rule = WorkflowTracableDecorator(Rule)
