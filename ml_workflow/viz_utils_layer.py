
class MlWorkflowNodeLayer:
    def __init__(self, node, origin = None, add_previous = False):
        if origin is None:
            origin = node.origin

        self.node = node if len(origin) == 1 else None
        self.layer_origin = origin[0]

        self.previous = []
        self.sub_layers = []
        # Not used for the moment
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
            self.previous.append(MlWorkflowNodeLayer(node, add_previous = True))

    def add_as_sub_layer(self, other_layer):
        assert(self.same_origin(other_layer))
        if len(other_layer.sub_layers) == 0:
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
        for layer in self.previous:
            res.extend(layer.get_all_root_layers())

        return res

# The purpose of this functions is mainly to the workflow node logic, which is that
# each node get a previous one and a next one 
def convert_node_to_layer(current_node):
    return MlWorkflowNodeLayer(current_node, add_previous = True)

