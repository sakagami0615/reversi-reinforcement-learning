from datetime import datetime


def get_current_datestr() -> str:
    """
    現在の時刻を「YYYY-MM-DD_HH-MM-SS-uuuuuu」形式の文字列として返却
    
    Returns:
        str: 現在の時刻を「YYYY-MM-DD_HH-MM-SS-uuuuuu」形式で表した文字列
        例: "2024-03-21_14-30-45-123456"
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S-%f")
