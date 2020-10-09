from .workflow_node import get_user_code_origine_workflow
from .workflow_node import WorkflowNode, WorkflowNodeRule

from .context_utils import get_current_rule

from .function_utils import prevent_exception

@prevent_exception
def handle_change(df, key):
    if df.ml_workflow_current_node is None:
        df.ml_workflow_current_node = get_user_code_origine_workflow()

    current_rule = get_current_rule()

    if df.ml_workflow_current_node.origin == current_rule:
        df.ml_workflow_current_node.add_modified_column(key)
    else:
        df.ml_workflow_current_node = WorkflowNodeRule(
            current_rule, 
            df.ml_workflow_current_node,
            modified_column = key
        )

# @prevent_exception
def handle_selection(df, key, other):
    if df.ml_workflow_current_node is None:
        df.ml_workflow_current_node = get_user_code_origine_workflow()

    current_rule = get_current_rule()

    other.ml_workflow_current_node = WorkflowNode(
        current_rule, 
        df.ml_workflow_current_node
    )
