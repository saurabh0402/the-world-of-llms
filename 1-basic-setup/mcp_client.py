from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.messages import ChatMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os
import asyncio
import json

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
    # model='hf.co/unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M',
    # model = 'gemma4:q4',
    model='hf.co/unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M',
    reasoning=True,
)
llm = llm.bind_tools(tools)

tool_mapper = {
    tool.name: tool for tool in tools
}

SYSTEM_MESSAGE = """
You are a helpful assistant.

You may call tools to answer the user's question.
When there are multiple messages, the first message is the user's question, the next messages are your responses
and tool call results. Your job is to use the messages to answer the user's query.

IMPORTANT: WHEN CALLING A TOOL REMEMBER TO PASS LIMITS TO PREVENT FETCHING A LOT OF DATA.

IMPORTANT RULES:

1. If you call a tool:
   - wait for the tool result
   - read the tool result carefully
   - use the tool result to answer the user

2. After receiving a ToolMessage:
   - NEVER ignore it
   - NEVER ask for the same information again
   - NEVER say the input is empty
   - ALWAYS base your final answer on the tool output

3. Tool results are factual and should be trusted.

4. Keep answers concise.

CRITICAL RULES:
- NEVER simulate, guess, or assume tool results
- NEVER roleplay receiving a tool response
- After calling a tool, output NOTHING — wait silently for the actual ToolMessage
- Only answer the user AFTER you have received a real ToolMessage
- Tool results will be provided to you automatically; do not invent them
"""

def get_llm_res(prompt: str) -> str:
    messages = [SystemMessage(SYSTEM_MESSAGE), HumanMessage(prompt)]
    print('----------------------------------------------------------')

    while True:
        full_content = None
        tool_calls = []
        thinking = False

        print('\033[92mMaking llm call...\033[0m')
        for chunk in llm.stream(messages):
            if chunk.additional_kwargs:
                if not thinking:
                    print('----------------------------------------------------------')
                    thinking = True
                print(f"\033[2m{chunk.additional_kwargs['reasoning_content']}\033[0m", end="", flush=True)

            if chunk.content:
                if thinking:
                    print('\n----------------------------------------------------------')
                    thinking = False

                print(chunk.content, end="", flush=True)

            if full_content:
                full_content += chunk
            else:
                full_content = chunk

        full_message = AIMessage(
            content = '',
            tool_calls = full_content.tool_calls,
        )
        messages.append(full_message)
        print()

        if len(full_message.tool_calls):
            print('----------------------------------------------------------')
            for tool_call in full_message.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']

                print(f'\033[92mCalling tool - "{tool_name}" with args - {tool_args}.\033[0m')

                res = asyncio.run(tool_mapper[tool_name].ainvoke(tool_args))
                messages.append(ToolMessage(content=json.dumps(res[0]['text']), tool_call_id=tool_call['id']))

                print('\033[92mTool call done!\033[0m')
            print('----------------------------------------------------------')
        else:
            break
    
    print('----------------------------------------------------------')

while True:
    print('> ', end='')
    ip = input()
    get_llm_res(ip)
