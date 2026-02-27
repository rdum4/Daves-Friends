from models.deck import Color
from services.lobby_service import LobbyService


class GameService:
    def __init__(self, lobby_service: LobbyService):
        self.lobby_service = lobby_service

    def play_card(
        self, channel_id: int, user_id: int, card_index: int, color: Color | None
    ):
        lobby = self.lobby_service.get_lobby(channel_id)
        lobby.game.play(user_id, card_index, color)

    def draw(self, channel_id: int, user_id: int):
        lobby = self.lobby_service.get_lobby(channel_id)
        lobby.game.draw_and_pass(user_id)
