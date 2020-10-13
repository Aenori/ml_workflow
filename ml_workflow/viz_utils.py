import os
import sys


try:
    # pydot-ng is a fork of pydot that is better maintained.
    import pydot_ng as pydot
except ImportError:
    # pydotplus is an improved version of pydot
    try:
        import pydotplus as pydot
    except ImportError:
        # Fall back on pydot if necessary.
        try:
            import pydot
        except ImportError:
            pydot = None


def check_pydot():
    """Returns True if PyDot and Graphviz are available."""
    if pydot is None:
        return False
    try:
        # Attempt to create an image of a blank graph
        # to check the pydot/graphviz installation.
        pydot.Dot.create(pydot.Dot())

        return True
    except (OSError, pydot.InvocationException):
        return False


def add_edge(dot, src, dst):
    if not dot.get_edge(src, dst):
        dot.add_edge(pydot.Edge(src, dst))


def model_to_dot(model,
                 show_shapes=False,
                 show_layer_names=True,
                 rankdir='TB',
                 expand_nested=False,
                 dpi=96,
                 subgraph=False):
    if not check_pydot():
        message = (
            'Failed to import pydot. You must `pip install pydot` '
            'and install graphviz (https://graphviz.gitlab.io/download/), ',
            'for `pydotprint` to work.'
        )

        if 'IPython.core.magics.namespace' in sys.modules:
            # We don't raise an exception here in order to avoid crashing
            # notebook
            # tests where graphviz is not available.
            print(message)
            return
        else:
            raise ImportError(message)

    if subgraph:
        dot = pydot.Cluster(style='dashed', graph_name=model.name)
        dot.set('label', model.name)
        dot.set('labeljust', 'l')
    else:
        dot = pydot.Dot()
        dot.set('rankdir', rankdir)
        dot.set('concentrate', True)
        dot.set('dpi', dpi)
        dot.set_node_defaults(shape='record')

    sub_n_first_node = {}
    sub_n_last_node = {}
    sub_w_first_node = {}
    sub_w_last_node = {}

    layers = model.get_all_nodes()

    for layer in layers:
        node = pydot.Node(layer.get_str_id(), label=str(layer))
        dot.add_node(node)

    # Connect nodes with edges.
    for layer in layers:
        layer_id = layer.get_str_id()

        for inbound_node in layer.parents:
            inbound_layer_id = inbound_node.get_str_id()
            assert dot.get_node(inbound_layer_id)
            assert dot.get_node(layer_id)
            add_edge(dot, inbound_layer_id, layer_id)
    return dot


def correct_weird_pydot_bug(filename):
    with open(filename, 'r') as f:
        content = f.read().replace('scale(1.3333 1.3333) ', '')
    with open(filename, 'w') as f:
        f.write(content)


def plot_model(model,
               to_file='model.svg',
               show_shapes=False,
               show_layer_names=True,
               rankdir='TB',
               expand_nested=False,
               dpi=96):
    dot = model_to_dot(model,
                       show_shapes=show_shapes,
                       show_layer_names=show_layer_names,
                       rankdir=rankdir,
                       expand_nested=expand_nested,
                       dpi=dpi)

    if dot is None:
        return

    _, extension = os.path.splitext(to_file)

    if not extension:
        extension = 'png'
    else:
        extension = extension[1:]

    # Save image to disk.

    dot.write(to_file, format=extension)

    if extension == 'svg':
        correct_weird_pydot_bug(to_file)

    # svg is useless here, but kept for clarity
    elif extension not in ('pdf', 'svg'):
        try:
            from IPython import display
            return display.Image(filename=to_file)

        except ImportError:
            pass
