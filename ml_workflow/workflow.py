
class RuleWorkflowNode(WorkflowNode):
    def __init__(self, current, parents = None):
        self.modified_columns = []
        super().__init__(current, parents)

class WorkflowNode:
    def __init__(self, current, parents = None):
        self.current = current
        self.parents = parents
