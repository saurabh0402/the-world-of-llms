from typing import TypedDict, Optional

class ToolResponse(TypedDict):
    success: bool
    content: Optional[str]
    error: Optional[str]
