from os.path import abspath

def source_path() -> str:
    return abspath(__file__).split('/utils')[0]

def base_path() -> str:
    return source_path().split('/src')[0]
