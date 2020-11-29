from .workflow_tracable import WorkflowTracable
import collections
from . import rule_reference
from . import rule_config_manager
from . import tracable_data_set
from . import execution_context

class Rule(WorkflowTracable):
    rule_by_name = collections.defaultdict(list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Rule.rule_by_name[self.name].append(self)
        rule_config_manager.RuleConfigManager.clean_reference_for(self.name)

    # Override Decorator.call_as_decorator
    def call_as_decorator(self, *args, **kwargs):
        super().call_as_decorator(*args, **kwargs)

        # On first call, check that if there is a RuleReference, the Rule has the same
        # arguments
        this_rule_reference = rule_reference.RuleReference.dict_by_name.get(self.name)
        if this_rule_reference:
            this_rule_reference.check_coherence(self)

    # This method is called by Decorator.__call__, after the first call,
    # as a decorator
    def call_as_decorated(self, *args, **kwargs):
        res = super().call_as_decorated(*args, **kwargs)

        # If res is a tracable type, but not an actual DataFrame, get it back
        with self:
            if self.return_tuple:
                res = tuple(map(lambda x : self.handle_result_type(x, args, kwargs), res))
            else:
                res = self.handle_result_type(res, args, kwargs)

        return res

    def handle_result_type(self, res, args, kwargs):
        if not tracable_data_set.is_tracable_raw_type(res):
            return res

        res = tracable_data_set.get_tracable_data_set(res)

        filter_tdf = lambda l: list(filter(tracable_data_set.is_tracable_data_set, l))

        res_previous = filter_tdf(args)
        res_previous.extend(filter_tdf(kwargs.values()))

        res.set_workflow_origin(
            execution_context.get_current_full_context(), 
            previous = res_previous
        )

        return res

    @classmethod
    def set_for_reference_name(_, name, rule):
        rule_config_manager.RuleConfigManager.set_for_reference_name(name, rule)

    @classmethod
    def get_from_reference_name(cls, name):
        return rule_config_manager.RuleConfigManager.get_from_reference_name(name)
