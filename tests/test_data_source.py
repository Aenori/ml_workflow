from common_import import *

from ml_workflow.data_source import mlwf_data_source

def test_frozen_arguments_removal():
    @mlwf_data_source(
        name='Exemple_simple_query',
        source_type='db',
        source='fake',
        frozen_ignore_args=['arg1', 'arg3']
    )
    def f(arg1, arg2, arg3, arg4):
        pass

    assert(f.frozen_ignore_args_positions == [2, 0])