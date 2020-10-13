from .workflow_tracable import WorkflowTracable, WorkflowTracableDecorator

class Rule(WorkflowTracable):
    pass

rule = WorkflowTracableDecorator(Rule)