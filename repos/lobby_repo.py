import discord

from models.game_state import GameState
from models.lobby_model import Lobby


class LobbyRepository:
    def __init__(self):
        self.lobbies: Dict[int, Lobby] = {}

    def get(self, id: int) -> Lobby:
        return self.lobbies[id]

    def set(self, id: int, user: discord.Interaction.user, game: GameState) -> None:
        self.lobbies[id] = Lobby(user, game, None)

    def delete(self, id: int) -> None:
        del self.lobbies[id]

    def exists(self, id: int) -> bool:
        return id in self.lobbies
