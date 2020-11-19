from . import rule

# Singleton class, only has static methods
class RuleConfigManager:
    cache_reference_name_to_rule = {}

    @classmethod
    def load_config(cls, config_filename):
        raise NotImplementedError()

    @classmethod
    def reset_config(cls):
        cls.use_default_branch = True
        cls.non_default_allowed_branch = set()
        cls.specific_rules = dict()

    @classmethod
    def clean_reference_for(cls, name):
        if name in cls.cache_reference_name_to_rule:
            del cls.cache_reference_name_to_rule[name]

    @classmethod
    def get_from_reference_name(cls, name):
        if name not in cls.cache_reference_name_to_rule:
            cls.cache_reference_name_to_rule[name] = cls.select_rule(name)

        return cls.cache_reference_name_to_rule[name]

    @classmethod
    def set_for_reference_name(cls, name, rule):
        cls.cache_reference_name_to_rule[name] = rule

    @classmethod
    def select_rule(cls, name):
        v = lambda r : r.__dict__.get('version', '')
        best_rule = None

        for irule in rule.Rule.rule_by_name[name]:
            if not hasattr(irule, 'branch'):
                if (best_rule is None) or (v(irule) > v(best_rule)):
                    best_rule = irule

        return best_rule

RuleConfigManager.reset_config()
