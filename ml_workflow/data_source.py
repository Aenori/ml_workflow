from .workflow_tracable import WorkflowTracable, WorkflowTracableDecorator
from .tracable_data_set import get_tracable_data_set


class DataSource(WorkflowTracable):
    AUTHORISED_ATTR = WorkflowTracable.AUTHORISED_ATTR.union(
        set(['frozen_ignore_args', 'source_type', 'source'])
    )

    def __init__(self, source_function, **kwargs):
        super().__init__(source_function, **kwargs)

        if 'frozen_ignore_args' in kwargs:
            self.frozen_ignore_args_positions = [
                source_function.__code__.co_varnames.index(arg)
                for arg in kwargs['frozen_ignore_args']
            ]
            # This is important, we will be removing these arguments
            self.frozen_ignore_args_positions.sort(reverse=True)

    def __call__(self, *args, **kwargs):
        result = self.call(*args, **kwargs)

        result = get_tracable_data_set(result)
        result.set_workflow_origin(self)
        result.ml_workflow_current_node.outside_len = len(result)

        return result

    # This function can be mocked by the session_recorder and
    # session_record_player
    def call(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    # Will probably include the version later on
    def get_qual_name(self):
        return self.name


mlwf_data_source = WorkflowTracableDecorator(DataSource)
