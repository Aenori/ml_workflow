
# The purpose of this functions is mainly to the workflow node logic, which is that
# each node get a previous one and a next one 
def convert_node_to_layer(model):
    return model.get_all_nodes()
