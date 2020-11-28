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

def test_rule_final_catch():
    @Rule(name='test2')
    def f(df):
        return pd.DataFrame({'A' : [1]})

    df = pd.DataFrame({'A' : [1]})
    res1 = f(df)
    
    assert(isinstance(res1, tds.TracableDataFrame))    
