from string import ascii_lowercase


def get_board_position_labels(board_size: int = 8) -> list[str]:
    """盤面の座標のラベル(8x8の場合はA1~H8までの文字列)を取得
    """
    if board_size <= 0 or board_size > len(ascii_lowercase):
        ValueError(f"The board size is not appropriate (board_size <= 0 || board_size > {len(ascii_lowercase)})")

    position_labels = []
    for i in range(board_size):
        row_label = str(i + 1)
        for j in range(board_size):
            col_label = chr(97 + j)
            position_labels.append(f"{col_label}{row_label}")
    
    return position_labels


def position_to_label(pos: tuple[int, int]) -> str:
    """座標をラベルに変換
    """
    col_label = chr(97 + pos[0])
    row_label = str(pos[1] + 1)
    return f"{col_label}{row_label}"


def label_to_position(label: str) -> tuple[int, int]:
    """ラベルを座標に変換
    """
    x = ord(label[0]) - 97
    y = int(label[1]) - 1
    return (x, y)
