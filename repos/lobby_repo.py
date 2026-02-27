"""
Provides storage for lobbies.
"""

import discord

from models.game_state import GameState
from models.lobby_model import Lobby


class LobbyRepository:
    """
    The lobby repository which stores, provides, modifies, and removes lobbies.
    """

    def __init__(self):
        self.lobbies: dict[int, Lobby] = {}

    def get(self, lobby_id: int) -> Lobby:
        """
        Returns a lobby based on its ID.
        """
        return self.lobbies[lobby_id]

    def set(
        self, lobby_id: int, user: discord.User, game: GameState
    ) -> None:
        """
        Stores a lobby by ID.
        """
        self.lobbies[lobby_id] = Lobby(user, game, None)

    def delete(self, lobby_id: int) -> None:
        """
        Deletes a lobby by ID.
        """
        del self.lobbies[lobby_id]

    def exists(self, lobby_id: int) -> bool:
        """
        Returns whether or not a lobby exists by ID.
        """
        return lobby_id in self.lobbies
