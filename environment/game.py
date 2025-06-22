from reversi import BitBoard, PyBitBoard
from reversi.player import Player

# TODO: この書き方だと修正面倒なので方法変えたい
# strategyクラスにメンバ変数追加するとか
IS_TRAIN_STRATEGIES = [
    "QLearnTrain"
]


def is_game_end(board: PyBitBoard):
    """盤面からゲーム終了を判定
    """
    return (not board.get_legal_moves("black")) and (not board.get_legal_moves("white"))


class Game:
    def __init__(self, board_size: int = 8):
        self._board_size = board_size

    def _decide(self, board: PyBitBoard, player: Player, opps_player: Player, episode: int):
        """次の行動を決定する。
        NOTE: 学習時、相手の行動が必要な場合があるため、[opps_player, episode] を引数指定できるようにしている
        TODO: 構成をもう少し扱いやすい形に変更したい
        """
        if type(player.strategy).__name__ in IS_TRAIN_STRATEGIES:
            return player.strategy.next_move(player.color, board, opps_player, episode)
        else:
            return player.strategy.next_move(player.color, board)


    def _move(self, board: PyBitBoard, player: Player, opps_player: Player, episode: int):
        player.move = self._decide(board, player, opps_player, episode)     # decide next move by strategy
        captures = board.put_disc(player.color, *player.move)               # put disc on board

        # bits to array
        player.captures.clear()
        size = board.size
        mask = 1 << (size*size-1)
        for y in range(size):
            for x in range(size):
                if captures & mask:
                    player.captures += [(x, y)]
                mask >>= 1
    
    def play(self, black_player: Player, white_player: Player, episode: int):
        board = BitBoard(self._board_size)
        while True:
            playable, foul_player = 0, None

            for curr_color in ["black", "white"]:
                # ターンプレイヤーと相手プレイヤーを変数に格納
                player      = black_player if curr_color == black_player.color else white_player
                opps_player = white_player if curr_color == black_player.color else black_player

                # 行動候補を取得
                legal_moves = board.get_legal_moves(player.color)
                if not legal_moves:
                    continue

                # 行動する
                self._move(board, player, opps_player, episode)
                if not player.captures:
                    foul_player = player
                    break

                playable += 1
            
            if foul_player:
                win_color = white_player.color if player.color == black_player.color else black_player.color
                result = self._get_result(win_color, board)
                break

            if playable == 0:
                win_color = self._judge_winner(board)
                result = self._get_result(win_color, board)
                break
        
        return result

    def _judge_winner(self, board: PyBitBoard) -> str:
        black_num, white_num = board._black_score, board._white_score
        win_color = "draw"
        if black_num > white_num:
            win_color = "black"
        elif black_num < white_num:
            win_color = "white"
        
        return win_color

    def _get_result(self, win_color: str, board: PyBitBoard):
        return {"winner": win_color, "n_black": board._black_score, "n_white": board._white_score}
