from pathlib import Path

def project_rooted(relative_path):
    cur_path = Path().resolve(__file__)
    return cur_path / relative_path