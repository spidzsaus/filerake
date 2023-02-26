class SuggestionTable:
    def __init__(self):
        self.rules = set()

    def add_pool(self, pool):
        self.rules.add(pool)
    
    def clear_pools(self):
        self.rules.clear()

    def feed_pools(self, pools):
        self.clear_pools()
        for pool in pools:
            self.add_pool(pool)

    def suggest(self, name):
        suggestions = set()
        for pool in self.rules:
            if pool.pattern.search(name):
                suggestions.add(pool)
        return suggestions