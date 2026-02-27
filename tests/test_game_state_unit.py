"""
Tests the game state class.
"""

import pytest

from models.game_state import GameState, GameError, Phase


def test_start_game_requires_two_players():
    """
    Game should not start with fewer than 2 players.
    """
    g = GameState()
    g.add_player(1)

    with pytest.raises(GameError):
        g.start_game()


def test_add_duplicate_player_raises_error():
    """
    Adding the same player twice should raise a GameError.
    """
    g = GameState()
    g.add_player(1)

    with pytest.raises(GameError):
        g.add_player(1)


def test_draw_advances_turn():
    """
    When a player draws and passes, the turn should move
    to the next player.
    """
    g = GameState()
    g.add_player(1)
    g.add_player(2)

    g.start_game()

    first_player = g.current_player()
    result = g.draw_and_pass(first_player, amt=1)

    assert result.next_player != first_player
    assert g.current_player() == result.next_player
    assert g.phase() == Phase.PLAYING

def test_add_bot():
    """
    Test adding a bot to a game, ensuring IDs are sequential negative integers.
    """
    g = GameState()
    g.add_player(1)
    g.add_bot()
    g.add_player(2)
    g.add_bot()
    g.add_bot()

    g.start_game()

    assert g.state["players"][1] == -1
    assert g.state["players"][3] == -2
    assert g.state["players"][4] == -3

def test_is_bot():
    """
    Ensure is_bot properly determines what is and is not a bot.
    """
    g = GameState()
    g.add_player(1)
    g.add_bot()
    g.add_player(2)
    g.add_bot()
    g.add_bot()

    players = g.state["players"]

    g.start_game()
    assert not g.is_bot(players[0])
    assert g.is_bot(players[1])
    assert not g.is_bot(players[2])
    assert g.is_bot(players[3])
    assert g.is_bot(players[4])


