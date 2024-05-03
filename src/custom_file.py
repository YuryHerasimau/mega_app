from utils.path_generation import create_file_path, create_file_name


def generate(filename: str, size_in_kb: int, file_extension: str, num_files: int):
    """
    Generate files with the given parameters.

    Parameters:
    - filename (str): The base name for the generated files.
    - size_in_kb (int): The size of each file in kilobytes.
    - file_extension (str): The extension of the generated files.
    - num_files (int): The number of files to generate.

    Returns:
    - None:The function does not return anything.
    """

    path = create_file_path(module_name=__name__)

    for i in range(num_files):
        # Convert kilobytes to bytes
        file_size_bytes = size_in_kb * 1024
        file_name = f"{filename}_{i}.{file_extension}"
        file_path = create_file_name(path=path, file_name=file_name)

        with open(file_path, "wb") as file:
            file.write(b"1" * file_size_bytes)
