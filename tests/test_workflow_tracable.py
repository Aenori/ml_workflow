from common_import import *

def test_rule_authorized_keys():
    # Just testing it doesn't raise exception
    @ml_workflow.rule(name = 'fake')
    def f():
        pass

    with utils.CheckRaisedError():
        @ml_workflow.rule(name = 'fake', source='fake')
        def f():
            pass

def test_data_source_authorized_keys():
    # Just testing it doesn't raise exception
    @ml_workflow.mlwf_data_source(name = 'fake', source='fake')
    def f():
        pass

    with utils.CheckRaisedError():
        @ml_workflow.mlwf_data_source(name = 'fake', source='fake', fake='fake')
        def f():
            pass