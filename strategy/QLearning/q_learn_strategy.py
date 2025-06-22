from typing import Union, Callable

from reversi.board import PyBitBoard
from reversi.move import Move
from reversi.player import Player
from reversi.strategies import AbstractStrategy

from strategy.QLearning.q_learn import QLearnCore, QLearnHyperParam
from environment.game import is_game_end
from common.get_board_position_labels import get_board_position_labels
from common.get_board_position_labels import position_to_label, label_to_position
from common.read_write import read_dict_pickle, write_dict_pickle
from common.create_logger import create_logger


logger = create_logger(__name__)


def get_state(color: str, board: PyBitBoard) -> tuple[str, str]:
    """状態を取得
    状態: ("black"|"white", "b|w|-" * 64)
    """
    return (color, board.get_board_line_info(color, 'b', 'w'))

def get_actions(color: str, board: PyBitBoard) -> list[str]:
    """行動候補リストを取得
    """
    return [position_to_label(p) for p in board.get_legal_moves(color)]

def get_reward(color: str, board: PyBitBoard) -> int:
    """報酬を取得
    """
    # ゲーム継続中は報酬無し(0)
    if not is_game_end(board):
        return 0

    n_black, n_white = board._black_score, board._white_score
    win_color = "black" if n_black > n_white else "white" if n_black < n_white else "draw"

    # 勝ち: 1, 負け: -1, 引分け: 0    
    reward = 0
    if win_color == color:
        reward = 1
    elif win_color != "draw":
        reward = -1

    return reward


class QLearnInfra(AbstractStrategy, QLearnCore):
    def __init__(self, read_q_table_file_path: str):
        super().__init__(
            action_list = get_board_position_labels(8),
            q_table = read_dict_pickle(read_q_table_file_path),
            is_learn = False
        )
    
    def next_move(self, color: str, board: PyBitBoard) -> Move:
        if board.size != 8:
            raise ValueError("Edax is only supported for 8x8 boards")
        
        # 状態と行動候補を取得する
        state = get_state(color, board)
        actions = get_actions(color, board)

        # 行動を確定
        action = self.policy(state, actions, episode=None)
        return label_to_position(action)


class QLearnTrain(AbstractStrategy, QLearnCore):
    def __init__(self, write_q_table_file_path: Union[None, str],
                       read_q_table_file_path: Union[str, None] = None,
                       param: QLearnHyperParam = QLearnHyperParam(),
                       init_q_value: Callable = lambda: float(0)):
        super().__init__(
            action_list = get_board_position_labels(8),
            q_table = self._init_q_table(read_q_table_file_path),
            is_learn = True,
            param = param,
            init_q_value = init_q_value
        )
        self._write_q_table_file_path = write_q_table_file_path
        if self._write_q_table_file_path is None:
            logger.warning("The output path for the q-table is not specified in the argument(write_q_table_file_path), so the q table will not be saved when processing ends.")
    
    def __del__(self):
        if self._write_q_table_file_path:
            write_dict_pickle(self.q_table, self._write_q_table_file_path)

    def _init_q_table(self, read_q_table_file_path: Union[str, None]) -> dict:
        if read_q_table_file_path:
            return read_dict_pickle(read_q_table_file_path)
        else:
            return {}
    
    def save_q_table(self):
        if self._write_q_table_file_path is None:
            raise ValueError("The output path for the q-table is not specified in the init argument(write_q_table_file_path).")
        write_dict_pickle(self.q_table, self._write_q_table_file_path)

    def next_move(self, color: str, board: PyBitBoard, opps_player: Player, episode: int) -> Move:
        if board.size != 8:
            raise ValueError("QLearning is only supported for 8x8 boards")
        
        # 状態と行動候補を取得する
        state = get_state(color, board)
        actions = get_actions(color, board)

        # 行動を確定 & 実施
        action = self.policy(state, actions, episode)
        board.put_disc(color, *label_to_position(action))

        # 相手の行動を実施
        n_undo = 1
        if get_actions(opps_player.color, board):
            opps_action = opps_player.strategy.next_move(opps_player.color, board)
            board.put_disc(opps_player.color, *opps_action)
            n_undo += 1

        # 次状態と報酬を求めテーブル更新
        next_state = get_state(color, board)
        reward = get_reward(color, board)
        self.update_q_table(state, action, next_state, reward)

        # 盤面を元に戻す
        for _ in range(n_undo):
            board.undo()

        return label_to_position(action)
