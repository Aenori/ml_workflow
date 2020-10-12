from .workflow_tracable import WorkflowTracable, WorkflowTracableDecorator
from .tracable_data_set import get_tracable_data_set

from .session import Session

class DataSource(WorkflowTracable):
    AUTHORISED_ATTR = WorkflowTracable.AUTHORISED_ATTR.union(set(['frozen_ignore_args']))
       
    def __call__(self, *args, **kwargs):
        if Session.has_active_recorder_player():
            return Session.handle_data_source(
                super().__call__,
                args,
                kwargs
            )
        
        return get_tracable_data_set(super().__call__(*args, **kwargs))

mlwf_data_source = WorkflowTracableDecorator(DataSource)
