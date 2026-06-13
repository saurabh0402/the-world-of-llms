from chat_loop import chat_loop

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

if __name__ == '__main__':
    chat_loop(get_existing_messages)
