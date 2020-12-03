from . import rule

# Singleton class, only has static methods
class RuleConfigManager:
    cache_reference_name_to_rule = {}
    user_set_reference_name_to_rule = {}

    @classmethod
    def load_config(cls, config_filename):
        raise NotImplementedError()

    @classmethod
    def reset_config(cls):
        # None is for default branch
        cls.allowed_branches = [None]
        cls.specific_rules = dict()

    @classmethod
    def add_branch(cls, branch):
        cls.allowed_branches.insert(0, branch)
        cls.cache_reference_name_to_rule = {}

    @classmethod
    def remove_branch(cls, branch):
        cls.allowed_branches.remove(branch)
        cls.cache_reference_name_to_rule = {}

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
    def set_for_reference_name(cls, name, rule_):
        cls.user_set_reference_name_to_rule[name] = rule_
        cls.cache_reference_name_to_rule[name] = rule_

    @classmethod
    def unset_for_reference_name(cls, name):
        if name in cls.user_set_reference_name_to_rule:
            del cls.user_set_reference_name_to_rule[name]
        if name in cls.cache_reference_name_to_rule:
            del cls.cache_reference_name_to_rule[name]

    @classmethod
    def config_to_str(cls):
        msg = f"  allowed branches => {cls.allowed_branches}\n"
        msg += f"  specific rules => {cls.specific_rules}"

        return msg

    @classmethod
    def is_first_rule_priority_to_second(cls, first_rule, second_rule):
        first_branch_index = cls.allowed_branches.index(first_rule.get_branch())
        second_branch_index = cls.allowed_branches.index(second_rule.get_branch())

        if first_branch_index != second_branch_index:
            # branch are classed by decreasing priority
            return first_branch_index < second_branch_index
        elif first_rule.get_version() is None:
            return False
        elif second_rule.get_version() is None:
            return True
        else:
            return first_rule.get_version() > second_rule.get_version()

    @classmethod
    def is_possible(cls, rule_):
        return rule_.get_branch() in cls.allowed_branches

    @classmethod
    def select_rule(cls, name):
        if name in cls.user_set_reference_name_to_rule:
            return cls.user_set_reference_name_to_rule[name]

        best_rule = None

        for irule in rule.Rule.rule_by_name[name]:
            if cls.is_possible(irule):
                if best_rule is None:
                    best_rule = irule
                elif cls.is_first_rule_priority_to_second(irule, best_rule):
                    best_rule = irule

        if best_rule is None:
            msg = f"ERROR : no rule found for {name}, please check the config"
            msg += cls.config_to_str()

            raise Exception(msg)

        return best_rule

RuleConfigManager.reset_config()
