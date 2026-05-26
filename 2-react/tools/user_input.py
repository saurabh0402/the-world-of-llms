from langchain.tools import tool
from typing import Optional

@tool
def ask_user(prompt: str) -> (bool, str, Optional[str]):
    """Ask user for any missing data.

    If there is any missing data, data you need from the user, or
    any clarification you need from the user, this tools can be used
    to get the required data.
    The given prompt is first displayed to the user and then the user
    can give the input for the same.
    
    Args:
        prompt (str) -> Prompt to be displayed to the user

    Return:
        Success (bool) -> Whether the operation was successful or not
        User Input (str) -> The input user provided
        Error (str) -> Any error in the operation
    """

    user_input = input(f'> {prompt}: ')
    return True, user_input, None

all_tools = [
    ask_user
]
