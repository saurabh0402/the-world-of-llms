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
                        'text': 'what is the weather in Bengaluru?'
                    }]
                }
            ]
            
            while True:
                response = client.chat.completions.create(
                    model='models/gemma-4-E4B-it-Q4_K_M.gguf',
                    messages=messages,
                    tools=mcp_tools,
                )

                message = response.choices[0].message
                messages.append(message)

                if not message.tool_calls:
                    print(message.content)
                    break

                for tool in message.tool_calls:
                    name = tool.function.name
                    args = json.loads(tool.function.arguments)

                    print(f'Calling tool {name} with args {tool.function.arguments}')

                    result = await session.call_tool(name, arguments=args)
                    messages.append({
                        "role": "tool_response",
                        "content": result.content[0].text,
                        "tool_call_id": tool.id,
                    })

if __name__ == '__main__':
    asyncio.run(main())
