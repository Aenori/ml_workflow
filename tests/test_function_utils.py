import python_path

from testfixtures import LogCapture
import utils
import pandas as pd
import numpy as np
import os

import ml_workflow
from ml_workflow.function_utils import prevent_exception
from ml_workflow.workflow_node import WorkflowNode


@prevent_exception
def failure():
    assert(False)


def test_prevent_exception():
    with LogCapture() as l:
        failure()

    l.check(
        ('ml_workflow.function_utils',
         'WARNING',
         'Encoutered error while processing failure, assert False'
         ))
