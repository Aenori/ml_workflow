
class MlWorkflowNodeLayer:
    def __init__(self, node, origin = None, add_previous = False):
        if origin is None:
            origin = node.origin

        self.node = node if len(origin) == 1 else None
        self.layer_origin = origin[0]

        self.previous_layers = []
        self.sub_layers = []

        self.merged_layers = []

        if len(origin) > 1:
            self.sub_layers.append(MlWorkflowNodeLayer(node, origin[1:]))

        if add_previous:
            self.add_all_previous_nodes(node.previous)

    def __str__(self):
        return str(self.node)

    def same_origin(self, other):
        return self.layer_origin == other.layer_origin

    def add_all_previous_nodes(self, node_list):
        for previous in node_list:
            self.add_previous_node(previous)

    def add_previous_node(self, node):
        if self.layer_origin == node.get_root_origin():
            self.add_as_sub_layer(MlWorkflowNodeLayer(node, add_previous = False))
            self.add_all_previous_nodes(node.previous)
        else:
            self.previous_layers.append(MlWorkflowNodeLayer(node, add_previous = True))

    def add_as_sub_layer(self, other_layer):
        assert(self.same_origin(other_layer))
        if len(other_layer.sub_layers) == 0:
            assert(other_layer.node is not None)
            if self.node is None:
                self.node = other_layer.node
            else:
                self.merged_layers.append(other_layer)
        else:
            assert(len(other_layer.sub_layers) == 1)
            other_sub_layer = other_layer.sub_layers[0]
            for sub_layer in self.sub_layers:
                if sub_layer.same_origin(other_sub_layer):
                    sub_layer.add_as_sub_layer(other_sub_layer)
                    break
            else:
                self.sub_layers.append(other_sub_layer)

    def get_all_root_layers(self):
        res = [self]
        for layer in self.previous_layers:
            res.extend(layer.get_all_root_layers())

        return res

    def get_all_depending_layers(self):
        for layer_list in (self.sub_layers, self.previous_layers):
            for layer in layer_list:
                yield layer

    def get_all_nodes(self):
        res = []
        if self.node:
            res.append(self.node)
        for layer in self.get_all_depending_layers():
            res.extend(layer.get_all_nodes())

        return res

    # Transformation from nodes to layers can result in merging duplicate node. For 
    # example, if we have something like :
    #   WorkflowNode(['Rule1']), WorkflowNode(['Rule1', 'Rule2']), WorkflowNode(['Rule1'])
    # That is, having Rule2 called inside Rule1 between two modifications, we want 
    # to have only two layer, Rule1 and Rule2, with Rule2 as sublayer of Rule1
    # Sofor the edge, we will need to redirect both edge id to the merge node
    def get_duplicated_id(self):
        res = {}
        for layer in self.merged_layers:
            assert(len(layer.sub_layers) == 0)
            res[layer.node.id] = self.node
        for layer in self.get_all_depending_layers():
            res.update(layer.get_duplicated_id())

        return res

    def get_all_included_node_id(self):
        res = set(self.get_duplicated_id().keys())
        res.update(node.id for node in self.get_all_nodes())

        return res

# The purpose of this functions is mainly to the workflow node logic, which is that
# each node get a previous one and a next one 
def convert_node_to_layer(current_node):
    return MlWorkflowNodeLayer(current_node, add_previous = True)

