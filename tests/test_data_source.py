import python_path

from ml_workflow.data_source import DataSource


def test_frozen_arguments_removal():
    @DataSource(
        name='Exemple_simple_query',
        source_type='db',
        source='fake',
        frozen_ignore_args=['arg1', 'arg3']
    )
    def f(arg1, arg2, arg3, arg4):
        pass

    assert(f.frozen_ignore_args_positions == [2, 0])
