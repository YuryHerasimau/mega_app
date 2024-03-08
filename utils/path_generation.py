import os


BASE_DIR = "output"


def create_file_path(module_name: str) -> str:
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    sub_dir = module_name.split('.')[1]
    
    path = os.path.join(BASE_DIR, sub_dir)
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def create_file_name(path: str, file_name: str) -> str:
    return os.path.join(path, file_name)