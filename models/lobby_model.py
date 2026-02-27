from dataclasses import dataclass

from discord.interactions import User

from models.game_state import GameState


@dataclass
class Lobby:
    user: User
    game: GameState
    main_message: int | None
