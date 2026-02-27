import importlib

from models import deck


def test_smoke_imports():
    """
    Smoke test: core modules should import without crashing.
    """
    modules = [
        "controllers",
        "models",
        "services",
        "repos",
        "ui",
        "utils",
        "views",
    ]

    for m in modules:
        importlib.import_module(m)


def test_smoke_deck_can_build_and_draw():
    """
    Smoke test: deck can be created and can draw at least one card.
    """
    if hasattr(deck, "Deck"):
        d = deck.Deck()
        assert d is not None

        if hasattr(d, "shuffle"):
            d.shuffle()

        if hasattr(d, "draw"):
            card = d.draw()
            assert card is not None
