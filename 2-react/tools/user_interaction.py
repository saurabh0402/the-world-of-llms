from langchain.tools import tool
from typing import Optional
import sys
from .types import ToolResponse

@tool
def ask_user(prompt: str) -> ToolResponse:
    """Ask user for any missing data.

    If there is any missing data, data you need from the user, or
    any clarification you need from the user, this tools can be used
    to get the required data.
    The given prompt is first displayed to the user and then the user
    can give the input for the same.
    
    Args:
        prompt (str) -> Prompt to be displayed to the user

    Return:
        success (bool) -> Whether the operation was successful or not
        content (str) -> The input user provided
        error (str) -> Any error in the operation
    """

    user_input = input(f'> {prompt}: ')
    return {
            "success": True,
            "content": user_input,
            "error": None,
        }

@tool
def exit():
    """Sends user a Bye and gracelly exits the application.
    
    Args:
        None

    Return:
        None
    """
    print('\nBye 👋')
    sys.exit(0)

all_tools = [
    ask_user,
    exit,
]
