import python_path

from ml_workflow.rule import Rule, RulePlaceHolder
import utils
from ml_workflow.workflow_node import WorkflowNode
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

def test_rule_placeholder():
    @Rule(name='test', version='v2')
    def f():
        return 0

    @Rule(name='test', version='v1')
    def g():
        return 1

    rph = RulePlaceHolder(name='test')

    assert(rph() == 0)
    Rule.set_for_reference_name('test', g)
    assert(rph() == 1)

