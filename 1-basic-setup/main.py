from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage, ToolMessage

@tool
def get_temperature(city: str) -> str:
    '''Returns the temperature at the given city

    Args:
        city (str) -> City to get the weather for
    '''
    return '30 degress celsius'

@tool
def get_precipitation(city: str) -> str:
    '''Returns the chances for precipitation
    
    Args:
        city (str) -> City to get the details for
    '''
    return '10 percent'

llm = ChatOllama(
    model='qwen3.5:4b',
    reasoning=False
)
llm = llm.bind_tools([get_temperature, get_precipitation])

tool_mapper = {
    'get_temperature': get_temperature,
    'get_precipitation': get_precipitation,
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

                res = tool_mapper[tool_name].invoke(tool_args)
                messages.append(ToolMessage(content=res, tool_call_id=tool_call['id']))
        else:
            return llm_res.content

while True:
    print('> ', end='')
    ip = input()
    print(get_llm_res(ip))