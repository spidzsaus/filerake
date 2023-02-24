import re

class SuggestionTable:
    def __init__(self):
        self.rules = dict()

    def add_rule(self, pool, rule):
        self.rules[rule] = pool

    def suggest(self, name):
        suggestions = set()
        for key, value in self.rules.items():
            if re.fullmatch(key, name):
                suggestions.add(value)
    



