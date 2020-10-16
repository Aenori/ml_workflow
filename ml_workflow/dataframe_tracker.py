from .workflow_node import get_user_code_origine_workflow
from .workflow_node import WorkflowNode, WorkflowNodeRule
from .tracable_data_set import TracableDataFrame, get_tracable_structure
from .context_utils import get_current_rule

from .function_utils import prevent_exception

# Should be migrated to using metaclass
class DataFrameTracker:
    def handle_setitem(self, super_method, tr_df, key, value):
        self.handle_in_place(super_method, tr_df, key, value)
        tr_df.ml_workflow_node.add_modified_key(key)

    def handle_merge(self, super_method, tr_df, right, *args, **kwargs):
        res = self.handle_with_return(super_method, tr_df, right, *args, **kwargs)
        right.set_default_ml_workflow_node_if_isnt_any()
        res.ml_workflow_node.parents.append(right.ml_workflow_node)

        return res

    def handle_in_place(self, super_method, tr_df, *args, **kwargs):
        super_method(tr_df, *args, **kwargs)
        tr_df.set_default_ml_workflow_node_if_isnt_any()

        current_rule = get_current_rule()

        if tr_df.ml_workflow_node.origin != current_rule:
            tr_df.ml_workflow_node = WorkflowNodeRule(
                current_rule,
                parents = tr_df.ml_workflow_node
            )

    def handle_with_return(self, super_method, tr_df, *args, **kwargs):
        result = super_method(tr_df, *args, **kwargs)
        result = get_tracable_structure(result.__class__)(result)
        tr_df.set_default_ml_workflow_node_if_isnt_any()

        current_rule = get_current_rule()

        if tr_df.ml_workflow_node.origin != current_rule:
            result.ml_workflow_node = WorkflowNodeRule(
                current_rule,
                parents = tr_df.ml_workflow_node
            )
            assert(result.ml_workflow_node is not None)
        else:
            result.ml_workflow_node = tr_df.ml_workflow_node
            assert(result.ml_workflow_node is not None)

        result.ml_workflow_node.outside_len = len(result)
        
        return result

    def add_notification_to(self, cls, method_name, hook_method):
        super_method = getattr(cls.__bases__[0], method_name)
    
        def tracable_method(self, *args, **kwargs):
            return hook_method(super_method, self, *args, **kwargs)
    
        setattr(cls, method_name, tracable_method)

    def init_df_monitoring(self):
        self.add_notification_to(TracableDataFrame, '__setitem__', self.handle_setitem)
        self.add_notification_to(TracableDataFrame, 'merge', self.handle_merge)
        self.add_notification_to(TracableDataFrame, '__getitem__', self.handle_with_return)


dataframe_tracker_singleton = DataFrameTracker()
dataframe_tracker_singleton.init_df_monitoring()



    
