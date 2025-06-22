from dataclasses import dataclass

from tqdm import tqdm

from reversi.strategies import AbstractStrategy
from environment.game import Game
from reversi.player import Player


@dataclass
class PlayerInfo:
    name: str
    strategy: AbstractStrategy


class Env:
    def __init__(self, board_size: int = 8):
        self._game = Game(board_size)

    def simulate(self, max_n_episode: int, black_player_info: PlayerInfo, white_player_info: PlayerInfo):
        black_player = Player("black", black_player_info.name, black_player_info.strategy)
        white_player = Player("white", white_player_info.name, white_player_info.strategy)

        result_history = []
        for episode in tqdm(range(1, max_n_episode + 1)):
            result = self._game.play(black_player, white_player, episode)
            result_history.append(result) 
        return result_history
