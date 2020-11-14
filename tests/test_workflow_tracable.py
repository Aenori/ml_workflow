import python_path

from utils.test_utils import CheckRaisedError
from ml_workflow.workflow_node import WorkflowNode
from ml_workflow.rule import Rule
from ml_workflow.data_source import DataSource
import ml_workflow
import pandas as pd
import numpy as np
import os


def test_rule_authorized_keys():
    # Just testing it doesn't raise exception
    @Rule(name='fake')
    def f():
        pass

    with CheckRaisedError():
        @ml_workflow.rule(name='fake', source='fake')
        def f():
            pass


def test_data_source_authorized_keys():
    # Just testing it doesn't raise exception
    @DataSource(name='fake', source='fake')
    def f():
        pass

    with CheckRaisedError():
        @DataSource(name='fake', source='fake', fake='fake')
        def f():
            pass
