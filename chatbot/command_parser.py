from pathlib import Path


def parse_input(user_input: str) -> tuple[str, str]:
    user_input_value = user_input.split()
    cmd, *args = user_input_value
    cmd = cmd.strip().lower()
    return cmd, *args


def read_file(path: str | Path = '') -> list:
    with open(path, 'r', encoding='utf-8') as fh:
        return [row.strip() for row in fh.readlines() if len(row.strip()) > 0]
