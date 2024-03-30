from pathlib import Path

from chatbot.constants import LEVEL_ERROR, INVALID_COMMAND


def parse_input(user_input: str) -> tuple[str, str]:
    try:
        user_input_value = user_input.split()
        cmd, *args = user_input_value
        cmd = cmd.strip().lower()
    except Exception:
        raise ValueError(LEVEL_ERROR + " " + INVALID_COMMAND)
    return cmd, *args


def read_file(path: str | Path = '') -> list:
    with open(path, 'r', encoding='utf-8') as fh:
        return [row.strip() for row in fh.readlines() if len(row.strip()) > 0]
