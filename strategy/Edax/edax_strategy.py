from typing import Union

import os
import json
import subprocess

from reversi.board import PyBitBoard
from reversi.move import Move
from reversi.strategies import AbstractStrategy
from common.get_os_name import get_os_name
from common.get_project_path import get_project_path


def get_edax_exe_name() -> str:
    """
    OSに応じて適切な実行ファイル名を取得
    """
    os_name = get_os_name()
    edax_exe = "wEdax-x86-64.exe" if os_name == "windows" else "lEdax-x86-64"
    return edax_exe


def check_processes(setting_file: str = None) -> None:
    """
    NOTE: processes数が1以上の場合、うまく動作しないので例外エラーを出す
    """
    if setting_file is None:
        return
    
    if os.path.isfile(setting_file):
        with open(setting_file, encoding="utf-8") as f:
            setting = json.load(f)
    
    if ("processes" in setting) and (setting["processes"] > 1):
        raise ValueError("Edax is only supported for processes=1")


class Edax(AbstractStrategy):
    
    EDAX_EXE = get_edax_exe_name()
    EDAX_PATH = os.path.abspath(os.path.join(get_project_path(), "service/edax-4.6", get_os_name()))
    BOARD_CACHE_PATH = os.path.abspath(os.path.join(get_project_path(), "service/edax-4.6/cache/board.txt"))

    def __init__(self, setting_file: Union[str, None]):
        check_processes(setting_file)

    def _run(self) -> str:
        """
        Edaxを実行して、次の手を取得
        """
        edax_cmd = f"{Edax.EDAX_EXE} -solve {Edax.BOARD_CACHE_PATH}"
        output_str = subprocess.run(edax_cmd, capture_output=True, text=True).stdout
        move = output_str.split('\n')[2][57:].split()[0]
        return move

    def next_move(self, color: str, board: PyBitBoard) -> Move:
        if board.size != 8:
            raise ValueError("Edax is only supported for 8x8 boards")

        # Edaxフォルダに移動
        # NOTE: Edax内でファイルを相対パスしているため、Edaxフォルダに移動して実行する
        prev_dir = os.getcwd()
        os.chdir(Edax.EDAX_PATH)

        # ボード情報をキャッシュファイルに保存
        os.makedirs(os.path.dirname(Edax.BOARD_CACHE_PATH), exist_ok=True)
        with open(Edax.BOARD_CACHE_PATH, 'w') as f:
            f.write(board.get_board_line_info(color))

        # Edaxを実行
        move = self._run()

        # 元のフォルダに戻る
        os.chdir(prev_dir)

        return Move(move)
