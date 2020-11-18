import python_path

from utils.decorator import ReferenceUsingTest
from utils.test_utils import compare_or_generate_ref
from ml_workflow.viz_utils import VizUtils, plot_model, \
    plot_model_full_detail, get_default_dirname
import utils
from ml_workflow.workflow_node import WorkflowNode
import ml_workflow
from ml_workflow import DataSource, Rule

from ml_workflow.execution_context import ExecutionContext

import shutil
import pandas as pd
import numpy as np
import os
import datetime as dt

@DataSource(name = 'test_data_source')
def data_source_test():
    """test_data_source doc string"""
    return pd.DataFrame({'A' : [1, 2], 'B' : [3, 4]})

@Rule(name = 'test_rule')
def rule_test(df):
    """test_rule doc string"""
    df['C'] = df['A'] + df['B']
    ExecutionContext.log("This is a log")
    return df

def get_df():
    df =  rule_test(data_source_test())

    return df

def test_plot_model_full_detail():
    df = get_df()

    ts = dt.datetime(year=2020, month=1, day=1)
    dirname = get_default_dirname(ts)

    # Cleaning, if there are some remnants of previous tests
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)
    
    df.plot_model_full_detail(ts = ts)

    assert(os.path.isdir(dirname))

    with open(os.path.join(dirname, 'test_rule.html'), 'r') as f:
        content = f.read()

    assert("test_rule doc string" in content)
    assert("This is a log" in content)

