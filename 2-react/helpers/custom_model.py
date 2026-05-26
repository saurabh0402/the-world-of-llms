from langchain_ollama import ChatOllama
from langchain.messages import AIMessage
from tools import all_tools

class CustomModel:
    def __init__(
        self,
        model='hf.co/unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M'
    ):
        _llm = ChatOllama(
            model=model,
            # reasoning=True,
        )

        self.tool_mappings = {
            tool.name: tool for tool in all_tools
        }
        self.llm = _llm.bind_tools(all_tools)

    def invoke(self, messages):
        thinking = False
        full_content = None

        for chunk in self.llm.stream(messages):
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

        if full_content.content:
            print()

        if full_content.tool_calls:
            return ('', full_content.tool_calls)

        return (full_content.content, [])
