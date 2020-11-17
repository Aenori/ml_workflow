
def write_detail_for_model(model, directory):
    layers = model.get_all_nodes()

    for layer in layers:
        write_html_information(layer, directory)

def write_html_information(layer, directory):
    return

    origin = layer.origin 

    template.write(
        code_source = None,
        logs = None,
        example = None,
        stats = None
    )
