from .workflow_tracable import WorkflowTracable, WorkflowTracableDecorator
from .tracable_data_set import get_tracable_data_set

class DataSource(WorkflowTracable):
    AUTHORISED_ATTR = WorkflowTracable.AUTHORISED_ATTR.union(
        set(['frozen_ignore_args', 'source_type', 'source'])
    )
       
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    # This function can be mocked by the session_recorder and session_record_player
    def call(self, *args, **kwargs)
        return get_tracable_data_set(super().__call__(*args, **kwargs))

mlwf_data_source = WorkflowTracableDecorator(DataSource)
