import asyncio
import json
from openai import OpenAI
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession

client = OpenAI(
    base_url='http://localhost:8080/v1',
    api_key='dummy'
)

async def main():
    print('Ask me something... > ', end='', flush=True)
    user_prompt = input()

    async with streamable_http_client('http://localhost:8000/mcp') as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            mcp_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema,
                    }
                }
                for t in tools.tools
            ]

            messages = [
                {
                    'role': 'system',
                    'content': [{
                        'type': 'text',
                        'text': '''
                            You are a helpful assistant whose job is to answer user's question as correctly
                            as possible.
                        ''',
                    }]
                },
                {
                    'role': 'user',
                    'content': [{
                        'type': 'text',
                        'text': user_prompt,
                    }]
                }
            ]
            
            while True:
                stream = client.chat.completions.create(
                    model='models/gemma-4-E4B-it-Q4_K_M.gguf',
                    messages=messages,
                    tools=mcp_tools,
                    stream=True
                )

                tool_calls = {}
                thinking = False
                outputting = False

                for chunk in stream:
                    delta = chunk.choices[0].delta

                    if getattr(delta, 'reasoning_content', None):
                        if not thinking:
                            print('\n\033[34m🤔 Thinking...\033[0m')
                            thinking = True
                        
                        print(f'\033[2m{delta.reasoning_content}\033[0m', end="", flush=True)
                    
                    if delta.content:
                        if not outputting:
                            print('\n------------------------------------------------------------------')
                            outputting = True

                        print(delta.content, end='', flush=True)

                    if delta.tool_calls:
                        for tc in delta.tool_calls:
                            index = tc.index

                            if index not in tool_calls:
                                tool_calls[index] = {
                                    'id': '',
                                    'name': '',
                                    'arguments': ''
                                }

                            if tc.id:
                                tool_calls[index]['id'] += tc.id

                            if tc.function and tc.function.name:
                                tool_calls[index]['name'] += tc.function.name

                            if tc.function.arguments:
                                tool_calls[index]['arguments'] += tc.function.arguments

                if not tool_calls:
                    break

                messages.append({
                    'role': 'assistant',
                    'content': None,
                    'tool_calls': [
                        {
                            'id': tc['id'],
                            'type': 'function',
                            'function': {
                                'name': tc['name'],
                                'arguments': tc['arguments'],
                            }
                        }
                        for tc in tool_calls.values()
                    ],
                })

                for tool in tool_calls.values():
                    name = tool['name']
                    args = tool['arguments']

                    print(f'\n\033[32m🛠️ Calling tool {name} with args {args}\033[0m', end='', flush=True)

                    result = await session.call_tool(name, arguments=json.loads(args))
                    messages.append({
                        "role": "tool_response",
                        "content": result.content[0].text,
                        "tool_call_id": tool['id']
                    })

if __name__ == '__main__':
    asyncio.run(main())
