from context import __SuggestionTable__

class Pool:
    @classmethod
    def from_json(cls, dic):
        new = cls()
        
        new.name = dic["name"]
        new.path = dic["path"]
        __SuggestionTable__.add_rule(new, dic["pattern"])
    
    def send(filepath):
        ...
        