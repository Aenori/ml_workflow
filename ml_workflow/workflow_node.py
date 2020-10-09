# Created by NRO 2020-10-09
#
# At the moment i am not using networkx because it is mainly working
# with graph, whereas i want to work mainly with node.
from enum import Enum

class WorkflowNode:
    def __init__(self, origin, parents = []):
        self.origin = origin
        if isinstance(parents, list):
            self.parents = parents
        elif isinstance(parents, WorkflowNode):
            self.parents = [parents]

    # Return the size of the graph where it is the last node
    def get_graph_size(self):
        return 1 + sum(map(WorkflowNode.get_graph_size, self.parents))

    def has_multiple_parents(self):
        return len(self.parents) > 1

    def get_previous_node(self):
        if self.has_multiple_parents():
            raise Exception("Attempt to call get_previous_node on node with several parents")

        if self.parents:
            return self.parents[0]

        return None

class WorkflowNodeRule(WorkflowNode):
    def __init__(self, rule, parents = [], modified_column = None):
        super().__init__(rule, parents)
        self.modified_columns = set()
        if modified_column:
            self.add_modified_column(modified_column)

    def add_modified_column(self, column):
        if isinstance(column, (int, str)):
            self.modified_columns.add(column)
        elif isinstance(column, (list, set)):
            self.modified_columns.update(column)
        else:
            raise Exception(f'Unknown column type {type(column)}')

class SpecialOrigin(Enum):
    USER_CODE = 0

def get_user_code_origine_workflow():
    return WorkflowNode(SpecialOrigin.USER_CODE)
