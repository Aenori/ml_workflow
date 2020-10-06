from .workflow_tracable import WorkflowTracable, WorkflowTracableDecorator
    
class Rule(WorkflowTracable):
    pass

mlwf_rule = WorkflowTracableDecorator(Rule)
