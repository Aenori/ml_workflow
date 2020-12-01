# Created by NRO 2020-10-09
#
# At the moment i am not using networkx because it is mainly working
# with graph, whereas i want to work mainly with node.
from enum import Enum
import itertools

from . import rule

class WorkflowNode:
    _next_id = 0

    @classmethod
    def get_next_id(cls):
        cls._next_id += 1
        
        return cls._next_id

    def __init__(self, origin, previous=[], tracable_item=None):
        # origin should be a list of applied WorfflowTracable (Rule and DataSource)
        assert(isinstance(origin, (tuple, list)))
        self.origin = tuple(origin)
        assert(len(origin) > 0)

        self.id = self.get_next_id()
        self.previous = previous if isinstance(previous, list) else [previous]

        for prev in self.previous:
            if not isinstance(prev, WorkflowNode):
                raise Exception(f"Uncompatible previous type received : {type(prev)}")

        self.logs = []
        self.stats = {}

        self.tracable_item = tracable_item

    def __str__(self):
        return str(self.get_leaf_origin())

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

    def match_origin(self, context):
        return self.origin[:len(context)] == context

    def get_leaf_origin(self):
        return self.origin[-1]

    def get_root_origin(self):
        return self.origin[0]

def get_user_code_origine_workflow(tracable_item = None):
    return WorkflowNode(origin = [rule.user_code_rule], tracable_item = tracable_item)
