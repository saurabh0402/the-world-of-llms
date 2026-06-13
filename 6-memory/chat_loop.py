from llm import call_llm

def chat_loop(get_existing_messages):
    messages = []

    while True:
        user_prompt = input('> ')
        new_messages = [{
            'role': 'user',
            'thinking': '',
            'content': user_prompt,
        }, {
            'role': 'assistant',
            'thinking': '',
            'content': '',
        }]

        thinking = False
        for data in call_llm(user_prompt, get_existing_messages(messages)):
            content = data['content']
            if data['type'] == 'thinking':
                if not thinking:
                    thinking = True

                print(f'\033[2m{content}\033[0m', end="", flush=True)
                new_messages[-1]['thinking'] += content
            else:
                if thinking:
                    thinking = False
                    print('\n----------------------------------------------------------')
                print(content, end="", flush=True)
                new_messages[-1]['content'] += content

        print('\n')
        messages = messages + new_messages
