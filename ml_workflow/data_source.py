from .workflow_tracable import WorkflowTracable, WorkflowTracableDecorator
from .tracable_data_set import get_tracable_data_set

class DataSource(WorkflowTracable):
    def __call__(self, *args, **kwargs):
        return get_tracable_data_set(super().__call__(*args, **kwargs))

mlwf_data_source = WorkflowTracableDecorator(DataSource)
