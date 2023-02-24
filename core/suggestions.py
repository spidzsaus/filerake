class SuggestionTable:
    def __init__(self):
        self.rules = set()

    def add_pool(self, pool):
        self.rules.add(pool)

    def suggest(self, name):
        suggestions = set()
        for pool in self.rules:
            if pool.pattern.search(name):
                suggestions.add(pool)
        return suggestions