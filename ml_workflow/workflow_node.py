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

    def __init__(self, origin, previous=[]):
        self.origin = origin
        self.id = self.get_next_id()
        self.previous = previous if isinstance(previous, list) else [previous]
        self.logs = []
        self.stats = {}

    def __str__(self):
        return str(self.origin)

    def get_str_id(self):
        return f'Workflow_node_{self.id}'

    # Return the size of the graph where it is the last node
    def get_graph_size(self):
        return 1 + sum(map(WorkflowNode.get_graph_size, self.previous))

    def has_multiple_previous(self):
        return len(self.previous) > 1

    def get_previous_node(self):
        if self.has_multiple_previous():
            raise Exception(
                "Attempt to call get_previous_node on"
                " node with several previous"
            )

        if self.previous:
            return self.previous[0]

        return None

    def get_all_nodes(self):
        res = [self]
        for parent in self.previous:
            res.extend(parent.get_all_nodes())
        return res

    def add_stat(self, key, value):
        self.stats[key] = value

    def add_log(self, log):
        self.logs.append(log)

    def add_logs(self, logs):
        self.logs.extend(logs)

    def formatted_stats(self):
        formatted_k_v = []
        for k, v in self.stats.items():
            if isinstance(v, float):
                formatted_k_v.append(f"{k} => {v:.3f}")
            else:
                formatted_k_v.append(f"{k} => {v}") 

        return '\n'.join(formatted_k_v)

class WorkflowNodeRule(WorkflowNode):
    def __init__(self, rule, previous=[]):
        super().__init__(rule, previous)
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
