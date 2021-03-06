import python_path

from ml_workflow.rule import no_context_rule
from ml_workflow.tracable_data_set import TracableDataFrame
import ml_workflow.tracable_data_set as tds
import utils
from ml_workflow.workflow_node import WorkflowNode
import ml_workflow
import pandas as pd
import numpy as np
import os
import sys


@ml_workflow.rule.Rule(name='fake')
def set_is_old_from_age(df):
    df['IsOld'] = df['Age'] > 60


def test_tracable_data_set():
    df = TracableDataFrame({'Age': [1, 67, 89, 10, 20]})

    df['Age'] += 1
    set_is_old_from_age(df)
    df['IsYoung'] = df['Age'] < 20
    assert(df.ml_workflow_node.get_graph_size() == 4)
    df['DansLaQuarantaine'] = np.logical_and(df['Age'] >= 40, df['Age'] < 50)

    assert(set(df.columns) == set(
        ['Age', 'IsYoung', 'IsOld', 'DansLaQuarantaine']))
    assert(df.ml_workflow_node.get_graph_size() == 4)

    assert(df.ml_workflow_node.get_leaf_origin() is no_context_rule)

    node = df.ml_workflow_node.get_previous_node()
    assert(node.get_leaf_origin() is set_is_old_from_age)

    node = node.get_previous_node()

    node = node.get_previous_node()
    assert(node.get_previous_node() is None)


def test_tracable_data_set_extract():
    df = TracableDataFrame({'Age': [1, 67, 89, 10, 20]})
    df_extract = df[df['Age'] > 30]
    assert(len(df_extract) == 2)
    assert(isinstance(df_extract, TracableDataFrame))

    assert(df_extract.ml_workflow_node.get_graph_size() == 2)

def test_merge():
    df1 = TracableDataFrame({'Id': [1,2], 'Age': [1, 67]})
    df2 = TracableDataFrame({'Id': [1,2], 'Size': [45, 167]})

    df3 = df1.merge(df2)
    assert(isinstance(df3, TracableDataFrame))
    assert(len(df3.ml_workflow_node.previous) == 2)
    assert(df3.ml_workflow_node.get_graph_size() == 3)

def test_merge_with_df():
    df1 = TracableDataFrame({'Id': [1,2], 'Age': [1, 67]})
    df2 = pd.DataFrame({'Id': [1,2], 'Size': [45, 167]})

    df3 = df1.merge(df2, on='Id')
    assert(isinstance(df3, TracableDataFrame))
    assert(len(df3.ml_workflow_node.previous) == 2)
    assert(df3.ml_workflow_node.get_graph_size() == 3)

def test_tracable_data_set_init():
    df = TracableDataFrame({'Age': [1, 67, 89, 10, 20]})
    assert(df.ml_workflow_node is None)

def test_is_tracable_type():
    assert(tds.is_tracable_type([]))
    assert(tds.is_tracable_type(tds.get_tracable_data_set([])))

def test_is_tracable_data_set():
    assert(not tds.is_tracable_data_set([]))
    assert(tds.is_tracable_data_set(tds.get_tracable_data_set([])))

def test_is_tracable_raw_type():
    assert(tds.is_tracable_raw_type([]))
    assert(not tds.is_tracable_raw_type(tds.get_tracable_data_set([])))

def test_sort_values_inplace():
    df = TracableDataFrame({'Id': [1,2], 'Age': [67, 1]})
    df.sort_values(by=['Age', 'Id'], inplace=True)
    
    assert((df['Id'] == [2, 1]).all())
    assert(isinstance(df, TracableDataFrame))

def test_sort_values_with_return():
    df = TracableDataFrame({'Id': [1,2], 'Age': [67, 1]})
    df = df.sort_values(by=['Age', 'Id'])

    assert((df['Id'] == [2, 1]).all())
    assert(isinstance(df, TracableDataFrame))    
