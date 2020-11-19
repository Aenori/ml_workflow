import python_path

from ml_workflow.rule_config_manager import RuleConfigManager
from ml_workflow.rule_reference import RuleReference
from ml_workflow.rule import Rule

import pytest

def clean_rule_for(name):
    if name in Rule.rule_by_name:
        del Rule.rule_by_name[name]
    if name in RuleReference.dict_by_name:
        del RuleReference.dict_by_name[name]

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    clean_rule_for('test_rule_reference')
    yield
    clean_rule_for('test_rule_reference')

def test_rule_reference():
    @Rule(name='test_rule_reference', version='v2')
    def f():
        return 0

    @Rule(name='test_rule_reference', version='v1')
    def g():
        return 1

    @Rule(name='test_rule_reference', version='v3', branch='other')
    def h():
        return 2

    @RuleReference(name='test_rule_reference')
    def rph(): pass

    assert(rph() == 0)
    RuleConfigManager.add_branch('undefined')
    assert(rph() == 0)
    RuleConfigManager.add_branch('other')
    assert(rph() == 2)    

