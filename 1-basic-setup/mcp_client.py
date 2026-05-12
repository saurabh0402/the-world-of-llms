from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

# Limiting tools else the local model hangs
ALLOWED_TOOLS = [
    # 'search_code',
    # 'search_issues',
    # 'search_pull_requests',
    'search_repositories',
    # 'search_users',
    # 'sub_issue_write'
]

mcp_client = MultiServerMCPClient(
    {
        "github": {
            "transport": "http",
            "url": "https://api.githubcopilot.com/mcp/",
            "headers": {
                "Authorization": f"Bearer {os.environ.get('GIT_PAT')}",
            }
        }
    }
)

tools = asyncio.run(mcp_client.get_tools())
tools = [
    tool for tool in tools
    if tool.name in ALLOWED_TOOLS
]

llm = ChatOllama(
    model='qwen3.5:4b',
    reasoning=False
)
llm = llm.bind_tools(tools)

tool_mapper = {
    tool.name: tool for tool in tools
}

def get_llm_res(prompt: str) -> str:
    messages = [HumanMessage(prompt)]
    while True:
        llm_res = llm.invoke(messages)
        messages.append(llm_res)

        if len(llm_res.tool_calls):
            for tool_call in llm_res.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']

                print(f'Calling tool - "{tool_name}" with args - {tool_args}.')

                res = asyncio.run(tool_mapper[tool_name].ainvoke(tool_args))
                messages.append(ToolMessage(content=res, tool_call_id=tool_call['id']))
        else:
            return llm_res.content

while True:
    print('> ', end='')
    ip = input()
    print(get_llm_res(ip))