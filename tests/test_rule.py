from ml_workflow import ml_rule

def test_ml_rule_with_args():
    @ml_rule(name = 'incrementation')
    def f(x):
        return x + 1

    assert(f(5) == 6)
    assert(f.name == 'incrementation')
    assert('def f(x):' in f.get_source())

@ml_rule
def g(x):
    return x + 2

print(g(5))
print(g.name)
print(g.get_source())