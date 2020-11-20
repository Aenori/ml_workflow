import python_path

from utils.decorator import ReferenceUsingTest
from utils.test_utils import compare_or_generate_ref
from ml_workflow.viz_utils import VizUtils, plot_model, \
    plot_model_full_detail, get_default_dirname
import utils
from ml_workflow.workflow_node import WorkflowNode
import ml_workflow
from ml_workflow import Rule, DataSource

import shutil
import pandas as pd
import numpy as np
import os
import datetime as dt


def get_simple_graph_with_fork():
    root1 = WorkflowNode(Rule(name='DataSource1'))
    root2 = WorkflowNode(Rule(name='DataSource2'))

    child1 = WorkflowNode(Rule(name='Processing_on_DS2'), previous=root2)
    merge_child2 = WorkflowNode(Rule(name='Merge_sources'), previous=[root1, child1])
    leaf_node = WorkflowNode(Rule(name='LeafNode'), previous=merge_child2)

    return leaf_node


def test_check_pydot():
    assert(VizUtils.check_pydot())


@ReferenceUsingTest('test_regression.svg')
def test_plot_model_as_svg():
    WorkflowNode._next_id = 0
    _test_plot_model('test_regression.svg')


@ReferenceUsingTest('test_regression.png')
def test_plot_model_as_png():
    _test_plot_model('test_regression.png')


def _test_plot_model(filename):
    leaf_node = get_simple_graph_with_fork()
    plot_model(leaf_node, filename, ts = 'TEST_ts')

    compare_or_generate_ref(filename)

def test_model_to_dot():
    leaf_node = get_simple_graph_with_fork()
    model_as_dot = VizUtils().model_to_dot(leaf_node)

    model_as_dot.write('test_regression.dot', format='dot')

def test_correct_weird_pydot_bug():
    with open('temp/correct_weird_pydot_bug', 'w') as f:
        f.write('transform="scale(1.33 1.33) rotate(0) translate(4 256)"')
    VizUtils.correct_weird_pydot_bug('temp/correct_weird_pydot_bug')
    with open('temp/correct_weird_pydot_bug', 'r') as f:
        assert(f.read() == 'transform="rotate(0) translate(4 256)"')

    with open('temp/correct_weird_pydot_bug', 'w') as f:
        f.write('transform="scale(1.3333 1.3333) rotate(0) translate(4 256)"')
    VizUtils.correct_weird_pydot_bug('temp/correct_weird_pydot_bug')
    with open('temp/correct_weird_pydot_bug', 'r') as f:
        assert(f.read() == 'transform="rotate(0) translate(4 256)"')    

def test_sub_graph():
    @DataSource(name='viz_util_data_source')
    def data_source():
        return pd.DataFrame({'A' : [1, 2, 3], 'B' : [3, 4, 5]})

    @Rule(name='viz_util_test_rule_1')
    def viz_util_test_rule_1(df):
        df['A'] += 1

        return df

    @Rule(name='viz_util_test_rule_2')
    def viz_util_test_rule_2(df):
        df['B'] += 2
        df = viz_util_test_rule_1(df)
        df['A'] *= 2

        return df

    df = viz_util_test_rule_2(data_source())
    df.plot_model('test_with_subgraph.png')

