import logging
from testfixtures import LogCapture

from common_import import *
from ml_workflow.function_utils import prevent_exception

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
