from pathlib import Path

from core.raking_piles import Pile


class SuggestionsManager:
    piles: list[Pile]

    def __init__(self, piles: list[Pile]) -> None:
        self.update_piles(piles)

    def update_piles(self, piles: list[Pile]) -> None:
        self.piles = piles
    
    def suggest(self, path: Path) -> list[Pile]:
        suggested_piles = []
        for pile in self.piles:
            if pile.pattern.search(str(path)):
                suggested_piles.append(pile)
        return suggested_piles