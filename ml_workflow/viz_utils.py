# Copyright 2018 The TensorFlow Authors. All Rights Reserved.

#

# Licensed under the Apache License, Version 2.0 (the "License");

# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

#

#     http://www.apache.org/licenses/LICENSE-2.0

#

# Unless required by applicable law or agreed to in writing, software

# distributed under the License is distributed on an "AS IS" BASIS,

# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

# See the License for the specific language governing permissions and

# limitations under the License.

# ==============================================================================

# pylint: disable=protected-access

# pylint: disable=g-import-not-at-top

"""Utilities related to model visualization."""

from __future__ import absolute_import

from __future__ import division

from __future__ import print_function


import os

import sys

# from tensorflow.python.keras.utils.io_utils import path_to_string

# from tensorflow.python.util import nest

# from tensorflow.python.util.tf_export import keras_export


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


def is_wrapped_model(layer):

    from tensorflow.python.keras.engine import functional

    from tensorflow.python.keras.layers import wrappers

    return (isinstance(layer, wrappers.Wrapper) and

            isinstance(layer.layer, functional.Functional))


def add_edge(dot, src, dst):

    if not dot.get_edge(src, dst):

        dot.add_edge(pydot.Edge(src, dst))


# @keras_export('keras.utils.model_to_dot')

def model_to_dot(model,

                 show_shapes=False,

                 show_layer_names=True,

                 rankdir='TB',

                 expand_nested=False,

                 dpi=96,

                 subgraph=False):
    """Convert a Keras model to dot format.

    Arguments:

        model: A Keras model instance.

        show_shapes: whether to display shape information.

        show_layer_names: whether to display layer names.

        rankdir: `rankdir` argument passed to PyDot,

                a string specifying the format of the plot:

                'TB' creates a vertical plot;

                'LR' creates a horizontal plot.

        expand_nested: whether to expand nested models into clusters.

        dpi: Dots per inch.

        subgraph: whether to return a `pydot.Cluster` instance.

    Returns:

        A `pydot.Dot` instance representing the Keras model or

        a `pydot.Cluster` instance representing nested model if

        `subgraph=True`.

    Raises:

        ImportError: if graphviz or pydot are not available.

    """

    if not check_pydot():

        message = (

            'Failed to import pydot. You must `pip install pydot` '

            'and install graphviz (https://graphviz.gitlab.io/download/), ',

            'for `pydotprint` to work.')

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


# @keras_export('keras.utils.plot_model')

def plot_model(model,

               to_file='model.svg',

               show_shapes=False,

               show_layer_names=True,

               rankdir='TB',

               expand_nested=False,

               dpi=96):
    """Converts a Keras model to dot format and save to a file.

    Example:

    ```python

    input = tf.keras.Input(shape=(100,), dtype='int32', name='input')

    x = tf.keras.layers.Embedding(

            output_dim=512, input_dim=10000, input_length=100)(input)

    x = tf.keras.layers.LSTM(32)(x)

    x = tf.keras.layers.Dense(64, activation='relu')(x)

    x = tf.keras.layers.Dense(64, activation='relu')(x)

    x = tf.keras.layers.Dense(64, activation='relu')(x)

    output = tf.keras.layers.Dense(1, activation='sigmoid', name='output')(x)

    model = tf.keras.Model(inputs=[input], outputs=[output])

    dot_img_file = '/tmp/model_1.png'

    tf.keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)

    ```

    Arguments:

        model: A Keras model instance

        to_file: File name of the plot image.

        show_shapes: whether to display shape information.

        show_layer_names: whether to display layer names.

        rankdir: `rankdir` argument passed to PyDot,

                a string specifying the format of the plot:

                'TB' creates a vertical plot;

                'LR' creates a horizontal plot.

        expand_nested: Whether to expand nested models into clusters.

        dpi: Dots per inch.

    Returns:

        A Jupyter notebook Image object if Jupyter is installed.

        This enables in-line display of the model plots in notebooks.

    """

    dot = model_to_dot(model,

                       show_shapes=show_shapes,

                       show_layer_names=show_layer_names,

                       rankdir=rankdir,

                       expand_nested=expand_nested,

                       dpi=dpi)

    #to_file = path_to_string(to_file)

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
