import collections

from .workflow_tracable import WorkflowTracable
from . import rule_reference
from . import rule_config_manager
from . import tracable_data_set
from . import execution_context
from .misc_utils import TimeIt

class Rule(WorkflowTracable):
    AUTHORISED_ATTR = WorkflowTracable.AUTHORISED_ATTR.union(set(['force_final_handling']))
    
    rule_by_name = collections.defaultdict(list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Rule.rule_by_name[self.name].append(self)
        rule_config_manager.RuleConfigManager.clean_reference_for(self.name)

    def set_default_values(self):
        self.force_final_handling = False
        super().set_default_values()

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
        if self.force_final_handling:
            self.temp_previous = self.extract_previous(args, kwargs)

        with TimeIt() as t:
            res = self.call(*args, **kwargs)

        # If res is a tracable type, but not an actual DataFrame, get it back
        if self.return_tuple:
            res = tuple(map(lambda x : self.handle_result_type(x, args, kwargs), res))
        else:
            res = self.handle_result_type(res, args, kwargs)

        # Rule can be used to return other things than a TracableDataSet
        if hasattr(res, 'ml_workflow_node'):
            res.ml_workflow_node.add_stat('duration', t.duration())
            res.ml_workflow_node.add_logs(execution_context.ExecutionContext.flush_logs())

        return res

    def extract_previous(self, args, kwargs):
        filter_tdf = lambda l: [
            arg.get_workflow_node_not_null() 
            for arg in filter(tracable_data_set.is_tracable_data_set, l)
        ]

        res_previous = filter_tdf(args)
        res_previous.extend(filter_tdf(kwargs.values()))

        return res_previous

    def handle_result_type(self, res, args, kwargs):
        if not self.force_final_handling:
            if not tracable_data_set.is_tracable_raw_type(res):
                return res

        res = tracable_data_set.get_tracable_data_set(res)

        if self.force_final_handling:
            res_previous = self.temp_previous
            del self.temp_previous
        else:
            res_previous = self.extract_previous(args, kwargs)

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
