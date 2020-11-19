import python_path
import ml_workflow.helper as helper

from IPython.core.display import HTML

def test_show_last_logs(capsys):
    res = helper.show_last_logs('test_rule')
    assert(isinstance(res, HTML))

    res = helper.show_last_logs('rule_test')
    out, err = capsys.readouterr()

    assert('ERROR' in err)
    assert('rule_test' in err)
