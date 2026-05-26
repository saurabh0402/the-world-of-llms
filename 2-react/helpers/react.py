from .custom_model import CustomModel
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.messages import ToolMessage, SystemMessage, HumanMessage, AIMessage

AGENT_INTRO_PROMPT = """
    You are a helpful AI Assitant whose aim to help the user by answering their
    questions and take actions for them.

    You have some tools available for you that you can use any time you want. When
    you run a tool, its response will be sent to you, post which you can decide
    if you want to make another set of tool calls or you have enough data to finally
    respond to the user with the final result.

    IMPORTANT INSTRUCTIONS
    - NEVER assume tool call results.
    - NEVER assume tools, use only those that are made available to you.
    - If you do not know an answer and do not have enough tools to take some action,
      say as such to the user. Do not assume things.
    - When there are more than 1 messages in a conversation, you are given all of them
      with the latest one being first followed by older and older messages.
""";


def get_react_agent():
    llm = CustomModel()

    def llm_call(state):
        messages = state['messages']
        content, tool_calls = llm.invoke(messages)
        return {
            "messages": [AIMessage(content=content, tool_calls=tool_calls)] + messages,
        }

    def tool_call(state):
        messages = state['messages']
        tool_calls = state['messages'][-1].tool_calls
        for tool_call in tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            print(f'\033[92mRunning tool - {tool_name} with args - {tool_args}\033[0m')
            tool = llm.tool_mappings[tool_name]
            tool_response = tool.invoke(tool_args)
            messages = [ToolMessage(content = tool_response, tool_call_id = tool_call['id'])] + messages

        return {
            "messages": messages,
        }

    def make_tool_call(state):
        last_message = state['messages'][-1]

        if last_message.tool_calls:
            return "tool_call"
        
        return END

    graph = StateGraph(MessagesState)
    graph.add_node("llm_call", llm_call)
    graph.add_node("tool_call", tool_call)
    graph.add_edge(START, "llm_call")
    graph.add_conditional_edges(
        "llm_call",
        make_tool_call,
        ["tool_call", END]
    )
    graph.add_edge("tool_call", "llm_call")
    agent = graph.compile()
    return agent


def run_agent(user_message):
    agent = get_react_agent()
    agent.invoke({
        "messages": [HumanMessage(user_message), SystemMessage(AGENT_INTRO_PROMPT)]
    })
