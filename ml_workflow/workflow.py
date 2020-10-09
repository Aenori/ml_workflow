# Created by NRO 2020-10-09
#
# At the moment i am not using networkx because it is mainly working
# with graph, whereas i want to work mainly with node.

class WorkflowNodeDataProcessing(WorkflowNode):
    def __init__(self, current, parents = []):
        self.modified_columns = []
        super().__init__(current, parents)

class WorkflowNode:
    def __init__(self, current, parents = []):
        self.current = current
        self.parents = parents

    # Return the size of the graph where it is the last node
    def get_graph_size(self):
        return 1 + sum(map(WorkflowNode.get_graph_size, self.parents))

