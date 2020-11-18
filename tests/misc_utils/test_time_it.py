from ml_workflow.misc_utils import TimeIt
import time

def test_time_it():
    with TimeIt() as t:
        time.sleep(0.07)

    assert(abs(t.duration() - 0.07) < 0.001)
