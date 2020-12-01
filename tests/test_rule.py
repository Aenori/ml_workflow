import python_path

from ml_workflow.rule import Rule
import utils
from ml_workflow.workflow_node import WorkflowNode
import ml_workflow.tracable_data_set as tds
import ml_workflow
import pandas as pd
import numpy as np
import os
import sys


def test_rule_with_args():
    @Rule(name='incrementation')
    def f(x):
        return x + 1

    assert(f(5) == 6)
    assert(f.name == 'incrementation')
    assert('def f(x):' in f.get_source())
    assert(isinstance(f, Rule))

@Rule(name='test_rule.test_catch')
def f1(df):
    return pd.DataFrame({'A' : [1]})

@Rule(name='test_rule.test_catch_2', return_tuple=True)
def f2(df):
    return (pd.DataFrame({'A' : [1]}), [])

def test_rule_final_catch_with_not_tracable():
    df = pd.DataFrame({'A' : [1]})
    res1 = f1(df)
    
    assert(isinstance(res1, tds.TracableDataFrame))
    assert(len(res1.ml_workflow_node.previous) == 0)

def test_rule_final_catch_with_tracable_positionnal():
    df = tds.TracableDataFrame({'A' : [1]})
    res1 = f1(df)

    assert(len(res1.ml_workflow_node.previous) == 1)
    assert(res1.ml_workflow_node.previous[0].tracable_item.columns == ['A'])

def test_rule_final_catch_with_tracable_named():
    df = tds.TracableDataFrame({'A' : [1]})
    res1 = f1(df = df)

    assert(len(res1.ml_workflow_node.previous) == 1)
    assert(res1.ml_workflow_node.previous[0].tracable_item.columns == ['A'])

def test_rule_final_catch_with_tracable_complex():
    df = tds.TracableDataFrame({'A' : [1]})
    res1 = f1([df])

    assert(res1.ml_workflow_node.previous == [])

def test_rule_return_tuple():
    df = tds.TracableDataFrame({'A' : [1]})
    res1 = f2(df)

    assert(isinstance(res1[0], tds.TracableDataFrame))
    assert(not isinstance(res1[1], tds.TracableDataFrame))

    assert(len(res1[0].ml_workflow_node.previous) == 1)
    assert(res1[0].ml_workflow_node.previous[0].tracable_item.columns == ['A'])

def test_force_final_handling():
    @Rule(name='temp1')
    def f(df):
        df['A'] += 1

        return df

    @Rule(name='temp2', force_final_handling=True)
    def g(df):
        df = f(df)
        df['B'] = df['A']

        return df

    df = tds.TracableDataFrame({'A' : [1]})

    df2 = g(df)
    # temp1 should not be recorded here
    assert(repr(list(map(lambda x : x.origin, df2.ml_workflow_node.get_all_nodes()))) == '[(temp2,), (generic.user_code,)]')
