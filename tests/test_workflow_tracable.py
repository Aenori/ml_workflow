import python_path

from ml_workflow.workflow_node import WorkflowNode
from ml_workflow.rule import Rule
from ml_workflow.data_source import DataSource
import ml_workflow
import pandas as pd
import numpy as np
import os

import pytest

def test_rule_authorized_keys():
    # Just testing it doesn't raise exception
    @Rule(name='fake')
    def f():
        pass

    with pytest.raises(Exception):
        @ml_workflow.rule(name='fake', source='fake')
        def f():
            pass


def test_data_source_authorized_keys():
    # Just testing it doesn't raise exception
    @DataSource(name='fake', source='fake')
    def f():
        pass

    with pytest.raises(Exception) as e:
        @DataSource(name='fake', source='fake', parameter_that_doesn_t_exist='fake')
        def f():
            pass

    assert('parameter_that_doesn_t_exist' in str(e.value))
