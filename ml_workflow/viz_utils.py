import os
import sys
import pydot

from .rule import Rule
from .data_source import DataSource

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
    raise_error_if_no_pydot()

    dot = get_dot_graph(subgraph, model, rankdir, dpi)
    layers = model.get_all_nodes()
    create_nodes(layers, dot)
    add_edges_in_dot(layers, dot)

    return dot


def add_edges_in_dot(layers, dot):
    for layer in layers:
        layer_id = layer.get_str_id()

        for inbound_node in layer.parents:
            inbound_layer_id = inbound_node.get_str_id()
            assert dot.get_node(inbound_layer_id)
            assert dot.get_node(layer_id)
            add_edge(dot, inbound_layer_id, layer_id)


def get_dot_graph(subgraph, model, rankdir, dpi):
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

    return dot


def raise_error_if_no_pydot():
    if not check_pydot():
        message = (
            'Failed to import pydot. You must `pip install pydot` '
            'and install graphviz (https://graphviz.gitlab.io/download/), ',
            'for `pydotprint` to work.'
        )

        if 'IPython.core.magics.namespace' in sys.modules:
            # We don't raise an exception here in order to avoid crashing
            # notebook tests where graphviz is not available.
            print(message)
            return
        else:
            raise ImportError(message)

def get_label(layer):
    label = str(layer)
    if hasattr(layer, 'outside_len'):
        label += f"\nsize : {layer.outside_len}"
    return label

def create_nodes(layers, dot):
    for layer in layers:
        origin = layer.origin 
        node = pydot.Node(
            layer.get_str_id(), 
            label=get_label(layer), 
            # Temporary for demo
            URL=f"http://www.google.fr/?q={layer}",
            shape=get_shape(origin),
            color=get_color(origin)
        )
        dot.add_node(node)

SHAPE_BY_CLASS = {
    Rule : 'diamond',
    DataSource : 'oval',
    'default': 'rectangle'
}

def get_shape(origin):
    try:
        return SHAPE_BY_CLASS[origin.__class__]
    except:
        return SHAPE_BY_CLASS['default']

def get_color(origin):
    try:
        if origin.highlight == 2:
            return 'red'
        elif origin.highlight == 1:
            return 'green'
        else:
            return 'grey'
    except AttributeError:
        return 'grey'

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
