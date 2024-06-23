import os


BASE_DIR = "output"


def create_file_path(module_name: str, base_dir: str = BASE_DIR) -> str:
    """
    Create a file path based on the provided module name.

    Args:
    - module_name (str): The name of the module used to create the file path.
    - base_dir (str): The base directory path where the file will be located. Default is 'output'.

    Returns:
    - str: The created file path.
    """

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    sub_dir = module_name.split(".")[1]

    path = os.path.join(base_dir, sub_dir)
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def create_file_name(path: str, file_name: str) -> str:
    """
    Function to create a file path by joining a directory path and a file name.

    Parameters:
    - path (str): The directory path where the file will be located.
    - file_name (str): The name of the file.

    Returns:
    - str: The complete file path after joining the directory path and file name
    """

    return os.path.join(path, file_name)
