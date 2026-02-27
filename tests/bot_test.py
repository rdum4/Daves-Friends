"""
Tests the bot model.
"""

from models.deck import Wild, Skip, Number, Color
from models import bot


def test_play_choose():
    """
    Ensure the bot can play the only available card.
    """
    top = Number(Color.YELLOW, 10)
    hand = [Wild(None), Number(Color.BLUE, 5), Number(Color.GREEN, 0), Skip(Color.RED)]

    (index, color) = bot.play_card(bot.Strategy.RANDOM, hand, top)

    assert index == 0
    assert color is not None
