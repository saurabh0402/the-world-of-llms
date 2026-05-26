from langchain.tools import tool
from pathlib import Path
from typing import Optional

# --------------------------
#        HELPERS
# --------------------------

def get_file_path(file_name: str, folder_path: str) -> Path:
    base_dir = Path(folder_path)
    file_path = base_dir.joinpath(file_name)
    return file_path

# --------------------------
#        TOOLS
# --------------------------

@tool
def create_folder(folder_path: str) -> (bool, Optional[str]):
    '''Create a folder at the specified path.
    It creates nested folder if required.
    Return True when the folder creation is successful.

    Args:
        folder_path (str) -> Path to create the folder at

    Return:
        Success (bool) -> Whether the operation was successful or not
        Error (str) -> The error message if any
    '''
    try:
        nested_folder = Path(folder_path)
        nested_folder.mkdir(parents=True, exist_ok=True)
        return True, None
    except Exception as e:
        return False, str(e)

@tool
def create_file(file_name: str, folder_path: str) -> (bool, Optional[str]):
    '''Create a file in the specified folder.

    Args:
        file_name (str) -> File name to create
        folder_path (str) -> Path of the folder to create the file in
    '''
    try:
        file_path = get_file_path(file_name, folder_path)
        file_path.touch()
        return True, None
    except Exception as e:
        return False, str(e)

@tool
def write_to_file(content: str, file_name: str, folder_path: str) -> (bool, Optional[str]):
    '''Write given content to the given file.

    Args:
        content (str) -> The content to write to the file
        file_name (str) -> File name to create
        folder_path (str) -> Path of the folder to create the file in
    '''
    try:
        file_path = get_file_path(file_name, folder_path)
        with open(file_path, 'w') as f:
            f.write(content)
        return True, None
    except Exception as e:
        return False, str(e)

all_tools = [
    create_folder, create_file, write_to_file
]
