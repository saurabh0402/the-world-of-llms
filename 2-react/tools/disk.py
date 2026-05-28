from langchain.tools import tool
from pathlib import Path
from typing import Optional
from .types import ToolResponse

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
def create_folder(folder_path: str) -> ToolResponse:
    '''Create a folder at the specified path.
    It creates nested folder if required.
    Return True when the folder creation is successful.

    Args:
        folder_path (str) -> Path to create the folder at

    Return:
        success (bool) -> Whether the operation was successful or not
        content (Optional[str]) -> Always None
        error (Optional[str]) -> The error message if any
    '''
    try:
        nested_folder = Path(folder_path)
        nested_folder.mkdir(parents=True, exist_ok=True)
        return {
            "success": True,
            "content": None,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "content": None,
            "error": str(e),
        }

@tool
def create_file(file_name: str, folder_path: str) -> (bool, Optional[str]):
    '''Create a file in the specified folder.

    Args:
        file_name (str) -> File name to create
        folder_path (str) -> Path of the folder to create the file in

    Return:
        success (bool) -> Whether the operation was successful or not
        content (Optional[str]) -> Always None
        error (Optional[str]) -> The error message if any
    '''
    try:
        file_path = get_file_path(file_name, folder_path)
        file_path.touch()
        return {
            "success": True,
            "content": None,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "content": None,
            "error": str(e),
        }

@tool
def write_to_file(content: str, file_name: str, folder_path: str) -> (bool, Optional[str]):
    '''Write given content to the given file.

    Args:
        content (str) -> The content to write to the file
        file_name (str) -> File name to create
        folder_path (str) -> Path of the folder to create the file in

    Return:
        success (bool) -> Whether the operation was successful or not
        content (Optional[str]) -> Always None
        error (Optional[str]) -> The error message if any
    '''
    try:
        file_path = get_file_path(file_name, folder_path)
        with open(file_path, 'w') as f:
            f.write(content)
        return {
            "success": True,
            "content": None,
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "content": None,
            "error": str(e),
        }

all_tools = [
    create_folder, create_file, write_to_file
]
