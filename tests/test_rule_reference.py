import python_path

from ml_workflow.rule_reference import RuleReference
from ml_workflow.rule import Rule

import pytest

def clean_rule_for(name):
    if name in Rule.rule_by_name:
        del Rule.rule_by_name[name]
    if name in Rule.reference_name_to_rule:
        del Rule.reference_name_to_rule[name]

def test_rule_reference():
    clean_rule_for('test_rule_reference')
    @Rule(name='test_rule_reference', version='v2')
    def f():
        return 0

    @Rule(name='test_rule_reference', version='v1')
    def g():
        return 1

    @RuleReference(name='test_rule_reference')
    def rph(): pass

    assert(rph() == 0)
    Rule.set_for_reference_name('test_rule_reference', g)
    assert(rph() == 1)

def test_rule_reference_with_version():
    clean_rule_for('test_rule_reference')
    # Checking version ordering is good, since as string "10.0" < "2.0"
    @Rule(name='test_rule_reference', version='10.0')
    def f():
        return 0

    @Rule(name='test_rule_reference', version='2.0')
    def g():
        return 1

    assert(f.version > g.version)

    @RuleReference(name='test_rule_reference')
    def rph(): pass

    assert(rph() == 0)
    Rule.set_for_reference_name('test_rule_reference', g)
    assert(rph() == 1)

def test_rule_reference_coherence_check_rule_first():
    @RuleReference(name='test_rule_reference_2')
    def rph(x, y): pass

    with pytest.raises(Exception):
        @Rule(name='test_rule_reference_2')
        def rule_that_fail(x): pass

def test_rule_reference_coherence_check_reference_first():
    @Rule(name='test_rule_reference_3')
    def rule_that_fail(x): pass

    with pytest.raises(Exception):
        @RuleReference(name='test_rule_reference_3')
        def rph(x, y): pass
