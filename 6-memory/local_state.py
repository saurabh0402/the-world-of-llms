from llm import call_llm

def get_existing_messages(messages):
    existing_msg_str = ''
    messages = messages[-6:]

    for message in messages:
        content = message['content']

        if message['role'] == 'user':
            existing_msg_str += f'''
user: {content}
            '''
        elif message['role'] == 'assistant':
            existing_msg_str += f'''
assistant: {content}
            '''

    return existing_msg_str

def main():
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

if __name__ == '__main__':
    main()