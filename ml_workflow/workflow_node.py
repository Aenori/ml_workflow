# Created by NRO 2020-10-09
#
# At the moment i am not using networkx because it is mainly working
# with graph, whereas i want to work mainly with node.
from enum import Enum
import itertools


class WorkflowNode:
    _next_id = 0

    @classmethod
    def get_next_id(cls):
        cls._next_id += 1
        
        return cls._next_id

    def __init__(self, origin, parents=[]):
        self.origin = origin
        self.id = self.get_next_id()
        self.parents = parents if isinstance(parents, list) else [parents]
        
    def __str__(self):
        return str(self.origin)

    def get_str_id(self):
        return f'Workflow_node_{self.id}'

    # Return the size of the graph where it is the last node
    def get_graph_size(self):
        return 1 + sum(map(WorkflowNode.get_graph_size, self.parents))

    def has_multiple_parents(self):
        return len(self.parents) > 1

    def get_previous_node(self):
        if self.has_multiple_parents():
            raise Exception(
                "Attempt to call get_previous_node on"
                " node with several parents"
            )

        if self.parents:
            return self.parents[0]

        return None

    def get_all_nodes(self):
        res = [self]
        for parent in self.parents:
            res.extend(parent.get_all_nodes())
        return res


class WorkflowNodeRule(WorkflowNode):
    def __init__(self, rule, parents=[]):
        super().__init__(rule, parents)
        self.modified_keys = set()

    def add_modified_key(self, key):
        if isinstance(key, (int, str)):
            self.modified_keys.add(key)
        elif isinstance(key, (list, set)):
            self.modified_keys.update(key)
        else:
            raise Exception(f'Unknown key type {type(key)}')


class SpecialOrigin(Enum):
    USER_CODE = 0


def get_user_code_origine_workflow():
    return WorkflowNode(SpecialOrigin.USER_CODE)
