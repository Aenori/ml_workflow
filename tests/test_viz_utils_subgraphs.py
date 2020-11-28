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
   
@Rule(name='viz_util_test_rule_1')
def viz_util_test_rule_1(df):
    df['A'] += 1

    return df

@Rule(name='viz_util_test_rule_2')
def viz_util_test_rule_2(df):
    df['B'] += 1

    return df

@ReferenceUsingTest('test_with_subgraph_1.svg')
def test_sub_graph_1():
    WorkflowNode._next_id = 0

    @DataSource(name='viz_util_data_source')
    def data_source():
        return pd.DataFrame({'A' : [1, 2, 3], 'B' : [3, 4, 5]})

    @Rule(name='viz_util_test_rule_3')
    def viz_util_test_rule_3(df):
        df['A'] *= 2
        df = viz_util_test_rule_1(df)
        df['A'] *= 2
        return df

    df = viz_util_test_rule_3(data_source())

    assert(len(df.ml_workflow_node.get_all_nodes()) == 3)

    assert(len(df.ml_workflow_node.get_all_nodes()[0].origin) == 2)
    assert(len(df.ml_workflow_node.get_all_nodes()[1].origin) == 1)
    assert(len(df.ml_workflow_node.get_all_nodes()[2].origin) == 1)

    df.plot_model('test_with_subgraph_1.svg')

@ReferenceUsingTest('test_with_subgraph_2.svg')
def test_sub_graph_2():
    WorkflowNode._next_id = 0

    @DataSource(name='viz_util_data_source')
    def data_source():
        return pd.DataFrame({'A' : [1, 2, 3], 'B' : [3, 4, 5]})

    @Rule(name='viz_util_test_rule_4')
    def viz_util_test_rule_4(df):
        df = viz_util_test_rule_1(df)
        df = viz_util_test_rule_2(df)
        return df

    df = viz_util_test_rule_4(data_source())

    assert(len(df.ml_workflow_node.get_all_nodes()))

    assert(len(df.ml_workflow_node.get_all_nodes()[0].origin) == 2)
    assert(len(df.ml_workflow_node.get_all_nodes()[1].origin) == 2)
    assert(len(df.ml_workflow_node.get_all_nodes()[2].origin) == 1)

    df.plot_model('test_with_subgraph_2.svg')

@ReferenceUsingTest('test_with_subgraph_3.svg')
def test_sub_graph_3():
    WorkflowNode._next_id = 0
    
    @DataSource(name='viz_util_data_source')
    def data_source():
        return pd.DataFrame({'A' : [1, 2, 3], 'B' : [3, 4, 5]})

    @Rule(name='viz_util_test_rule_4')
    def viz_util_test_rule_4(df):
        df = viz_util_test_rule_1(df)
        df = viz_util_test_rule_2(df)
        return df

    @Rule(name='viz_util_test_rule_5')
    def viz_util_test_rule_5(df):
        df = viz_util_test_rule_1(df)
        df = viz_util_test_rule_4(df)

        return df

    df1 = data_source()
    df2 = viz_util_test_rule_4(df1)
    df3 = viz_util_test_rule_5(df2)

    assert(len(df3.ml_workflow_node.get_all_nodes()) == 6)

    df3.plot_model('test_with_subgraph_3.svg')
