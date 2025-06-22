import platform


def get_os_name() -> str:
    """
    Get the name of the operating system.
    """
    system = platform.system()

    if system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "mac"
    elif system == "Linux":
        return "linux"
    else:
        raise ValueError(f"Invalid OS: {system}")
