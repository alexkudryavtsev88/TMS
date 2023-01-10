from pathlib import Path

ROOT_DIR = 'me'


def get_root():
    cur_path = Path(__file__)
    while cur_path.name != ROOT_DIR:
        cur_path = cur_path.parent
    return cur_path


print(get_root())