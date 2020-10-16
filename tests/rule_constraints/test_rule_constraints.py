import sys, os
sys.path.append(os.getcwd())

from ml_workflow import DataSource
from ml_workflow import Rule
from ml_workflow.rule_constraints import MustBeCalledAfter, MustNotBeCalledAfter

import pandas as pd
import numpy as np

@Rule(name='fake1')
def f(df):
    df['age'][df['age'].isna()] = df['age'].mean()
    return df

@Rule(name='fake2', constraints=MustNotBeCalledAfter(f))
def g(df):
    return df[df['age'] >18]

@DataSource(name='fake3')
def get_test_df():
    return pd.DataFrame(
            {'age' : [np.nan, 20, np.nan, 8, 80]}
        )

def test_must_not_be_called_after():
    seq_to_tests = [[f], [g], [f, g], [g, f]]
    expected_results = [True, True, True, False]

    for seq_to_test, expected_result in zip(seq_to_tests, expected_results):
        df = get_test_df()
        for func in seq_to_test:
            df = func(df)

        df.check_workflow()
        print(df.ml_workflow_current_node.get_graph_size())
        print([wf_tracable.origin.name for wf_tracable in df.ml_workflow_current_node.get_all_nodes()])
        assert(df.is_valid == expected_result)

@Rule(name='fake4', constraints=MustBeCalledAfter(f))
def g2(df):
    return df[df['age'] >18]

def test_must_be_called_after():
    tests = [f, g2, lambda df : f(g2(df)), lambda df : g2(f(df))]
    expected_results = [True, False, False, True]

    for test, expected_result in zip(tests, expected_results):
        df = get_test_df()
        df = test(df)
        df.check_workflow()
        # assert(df.is_valid == expected_result)