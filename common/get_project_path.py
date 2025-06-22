import os


def get_project_path() -> str:
    return os.path.abspath(os.path.dirname(__file__) + "/..")
