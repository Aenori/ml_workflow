from ..rule import Rule
import logging
logger = logging.getLogger(__name__)

class RuleConstraint:
    def check(self, caller, previous_wf_trackable):
        raise NotImplementedError

class MustBeCalledAfter(RuleConstraint):
    def __init__(self, other_rules):
        if isinstance(other_rules, Rule):
            self.other_rules = [other_rules]
        else:
            self.other_rules = other_rules

    def check(self, caller, previous_wf_trackable):
        valid = False
        print((previous_wf_trackable, self.other_rules))
        for wf_trackable in previous_wf_trackable:
            for other_rule in self.other_rules:
                if other_rule.match(wf_trackable):
                    valid = True
                    logger.warning(f"{caller} : constraint {self.__class__.__name__} is not satisfied")

        return valid

class MustNotBeCalledAfter(MustBeCalledAfter):
    def check(self, caller, previous_wf_trackable):
        return not super().check(caller, previous_wf_trackable)

