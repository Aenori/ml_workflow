import os
import sys
import pydot

import datetime as dt
import re

import IPython
from IPython.display import SVG, display

from . import viz_utils_node_detail_writer
from . import viz_utils_layer

class VizUtils:
    rankdir = 'TB'
    dpi = 96
    
    SHAPE_BY_CLASS_NAME = {
        'Rule' : 'rectangle',
        'DataSource' : 'cylinder',
        'default': 'ovale'
    }

    @staticmethod
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

    @staticmethod
    def raise_error_if_no_pydot():
        if not VizUtils.check_pydot():
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

    @staticmethod
    def add_edge(dot, src, dst):
        if not dot.get_edge(src, dst):
            dot.add_edge(pydot.Edge(src, dst))

    @staticmethod
    def get_label(layer):
        label = str(layer)
        if hasattr(layer, 'outside_len'):
            label += f"\nsize : {layer.outside_len}"
        return label

    @staticmethod
    def get_shape(origin):
        try:
            return VizUtils.SHAPE_BY_CLASS_NAME[origin.__class__.__name__]
        except:
            return VizUtils.SHAPE_BY_CLASS_NAME['default']

    @staticmethod
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

    @staticmethod
    def correct_weird_pydot_bug(filename):
        with open(filename, 'r') as f:
            content = f.read()
        with open(filename, 'w') as f:
            # The \\1 means the same number of 3 as in the first group
            f.write(re.sub("scale\(1\.(3+) 1\.\\1\) ", '', content))

    def __init__(self, ts = None, expand_nested = True):
        self.ts = ts if ts else dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.expand_nested = expand_nested

    def model_to_dot(self, model, subgraph=False):
        self.raise_error_if_no_pydot()

        dot = self.get_dot_graph(subgraph, model)
        layers = viz_utils_layer.convert_node_to_layer(model).get_all_root_layers()
        nodes = model.get_all_nodes()
        self.create_nodes(layers, dot)
        self.add_edges_in_dot(nodes, dot)

        return dot

    def add_edges_in_dot(self, layers, dot):
        for layer in layers:
            layer_id = layer.get_str_id()

            for inbound_node in layer.previous:
                inbound_layer_id = inbound_node.get_str_id()
                assert dot.get_node(inbound_layer_id)
                assert dot.get_node(layer_id)
                self.add_edge(dot, inbound_layer_id, layer_id)


    def get_dot_graph(self, subgraph, model):
        if subgraph:
            dot = pydot.Cluster(style='dashed', graph_name=model.name)
            dot.set('label', model.name)
            dot.set('labeljust', 'l')
        else:
            dot = pydot.Dot()
            dot.set('rankdir', self.rankdir)
            dot.set('concentrate', True)
            dot.set('dpi', self.dpi)
            dot.set_node_defaults(shape='record')

        return dot

    def create_nodes(self, layers, dot):
        for layer in layers:
            if len(layer.sub_layers):
                origin = layer.layer_origin
                print(f"Origin type : {origin} {type(origin)}")
                cluster = pydot.Cluster(style='dashed', graph_name=str(origin))
                if layer.node is not None:
                    self.create_dot_node(cluster, layer)
                self.create_nodes(layer.sub_layers, cluster)
            else:
                assert(layer.node is not None)
                self.create_dot_node(dot, layer)

    def create_dot_node(self, dot, layer):
        origin = layer.layer_origin 
        node = pydot.Node(
            layer.node.get_str_id(), 
            label=self.get_label(layer.node), 
            # Temporary for demo
            URL=f"http://www.google.fr/?q={layer}",
            shape=self.get_shape(origin),
            color=self.get_color(origin)
        )
        dot.add_node(node)

    def plot_model(self,
                   model,
                   to_file):
        dot = self.model_to_dot(model)

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
            self.correct_weird_pydot_bug(to_file)
            return SVG(to_file)
        # svg is useless here, but kept for clarity
        elif extension not in ('pdf', 'svg'):
            try:
                return IPython.display.Image(filename=to_file)

            except ImportError:
                pass

DEFAULT_DIR_NAME_PREFIX = 'ml_workflow_graph_detail'

def get_default_dirname(ts):
    return f"{DEFAULT_DIR_NAME_PREFIX}_{ts.strftime('%Y%m%d_%H%M%S')}"

def plot_model_full_detail(model, directory = None, expand_nested=True, ts = None):
    if ts is None:
        ts = dt.datetime.now()
    if directory is None:
        directory =  os.path.join(os.getcwd(), get_default_dirname(ts))
    if not os.path.isdir(directory):
        os.mkdir(directory)

    to_file = os.path.join(directory, 'main_graph.svg')
    viz_utils_node_detail_writer.write_detail_for_model(model, directory = directory)

    return VizUtils(expand_nested=expand_nested, ts=ts).plot_model(model, to_file)

def plot_model(model, to_file='model.png', expand_nested=True, ts=None):
    """Plot_model is creating an image of the model, representing the differents
 steps, datasource, and so on"""

    return VizUtils(expand_nested=expand_nested, ts=ts).plot_model(model, to_file)
