import re

class SuggestionTable:
    def __init__(self):
        self.rules = dict()

    def add_rule(self, pool, rule):
        self.rules[rule] = pool

    def suggest(self, name):
        suggestions = set()
        for key, value in self.rules.items():
            pattern = re.compile(key, re.UNICODE)
            if pattern.search(name):
            #if key in name:
                suggestions.add(value)
        return suggestions



