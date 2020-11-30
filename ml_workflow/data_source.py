
from .workflow_tracable import WorkflowTracable
from .tracable_data_set import get_tracable_data_set
from .misc_utils import TimeIt
from . import execution_context

class DataSource(WorkflowTracable):
    AUTHORISED_ATTR = WorkflowTracable.AUTHORISED_ATTR.union(
        set(['frozen_ignore_args', 'source_type', 'source'])
    )

    def call(self, *args, **kwargs):
        result = self.hookable_call(*args, **kwargs)

        result = get_tracable_data_set(result)
        result.set_workflow_origin([self])
        result.ml_workflow_node.outside_len = len(result)

        return result

    # This function can be mocked by the session_recorder and
    # session_record_player
    def hookable_call(self, *args, **kwargs):
        return super().call(*args, **kwargs)

    # Will probably include the version later on
    def get_qual_name(self):
        return self.name

    def call_as_decorator(self, *args, **kwargs):
        super().call_as_decorator(*args, **kwargs)

        if hasattr(self, 'frozen_ignore_args'):
            self.handle_frozen_ignore_args(self.frozen_ignore_args)
    
    # This method is called by Decorator.__call__, after the first call,
    # as a decorator
    def call_as_decorated(self, *args, **kwargs):
        with TimeIt() as t:
            res = self.call(*args, **kwargs)

        # Rule can be used to return other things than a TracableDataSet
        if hasattr(res, 'ml_workflow_node'):
            res.ml_workflow_node.add_stat('duration', t.duration())
            res.ml_workflow_node.add_logs(execution_context.ExecutionContext.flush_logs())

        return res

    def handle_frozen_ignore_args(self, frozen_ignore_args):
        self.frozen_ignore_args_positions = [
                self.source_function.__code__.co_varnames.index(arg)
                for arg in frozen_ignore_args
            ]
        
        # This is important, we will be removing these arguments
        self.frozen_ignore_args_positions.sort(reverse=True)
