import importlib


def test_smoke_imports():
    """
    Smoke test: core modules should import without crashing.
    """
    modules = [
        "models.deck",
        "models.game_state",
        "services.lobby_service",
    ]

    for m in modules:
        importlib.import_module(m)


def test_smoke_deck_can_build_and_draw():
    """
    Smoke test: deck can be created and can draw at least one card.
    """
    from models import deck

    if hasattr(deck, "Deck"):
        d = deck.Deck()
        assert d is not None

        if hasattr(d, "shuffle"):
            d.shuffle()

        if hasattr(d, "draw"):
            card = d.draw()
            assert card is not None
