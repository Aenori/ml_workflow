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
def f(df):
    return pd.DataFrame({'A' : [1]})

def test_rule_final_catch_with_not_tracable():
    df = pd.DataFrame({'A' : [1]})
    res1 = f(df)
    
    assert(isinstance(res1, tds.TracableDataFrame))
    assert(len(res1.ml_workflow_node.previous) == 0)

def test_rule_final_catch_with_tracable_positionnal():
    df = tds.TracableDataFrame({'A' : [1]})
    res1 = f(df)

    assert(len(res1.ml_workflow_node.previous) == 1)
    assert(res1.ml_workflow_node.previous[0].columns == ['A'])

def test_rule_final_catch_with_tracable_named():
    df = tds.TracableDataFrame({'A' : [1]})
    res1 = f(df = df)

    assert(len(res1.ml_workflow_node.previous) == 1)
    assert(res1.ml_workflow_node.previous[0].columns == ['A'])

def test_rule_final_catch_with_tracable_complex():
    df = tds.TracableDataFrame({'A' : [1]})
    res1 = f([df])

    assert(res1.ml_workflow_node.previous == [])

