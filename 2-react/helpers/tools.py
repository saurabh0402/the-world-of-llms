from langchain.tools import tool
from pathlib import Path

@tool
def create_folder(folder_path: str) -> bool:
    '''Create a folder at the specified path.
    It creates nested folder if required.
    Return True when the folder creation is successful.

    Args:
        folder_path (str) -> Path to create the folder at
    '''
    nested_folder = Path(folder_path)
    nested_folder.mkdir(parents=True, exist_ok=True)
    return True

@tool
def create_file(file_name: str, folder_path: str) -> bool:
    '''Create a file in the specified folder.

    Args:
        file_name (str) -> File name to create
        folder_path (str) -> Path of the folder to create the file in
    '''
    base_dir = Path(folder_path)
    file_path = base_dir.joinpath(file_name)
    file_path.touch()
    return True

all_tools = [
    create_folder, create_file
]

tools_mapping = {
    tool.name: tool for tool in all_tools
}
