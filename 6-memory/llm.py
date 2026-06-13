from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:8080/v1',
    api_key='dummy'
)

def call_llm(user_prompt: str, existing_messages: str = ''):
    messages = [
        {
            'role': 'system',
            'content': [{
                'type': 'text',
                'text': '''
                    You are a helpful assistant whose job is to answer user's question as correctly
                    as possible. You are given a history of the existing conversation and then the
                    current user question. Answer the user's current question. Use any context or
                    details from the existing conversation as needed.
                ''',
            }]
        },
        {
            'role': 'system',
            'content': [{
                'type': 'text',
                'text': f'''
                    Chat History:
                    {existing_messages}
                    ---
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

    stream = client.chat.completions.create(
        model='models/gemma-4-E4B-it-Q4_K_M.gguf',
        messages=messages,
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta

        if getattr(delta, 'reasoning_content', None):
            yield {
                'type': 'thinking',
                'content': delta.reasoning_content,
            }
        
        if delta.content:
            yield {
                'type': 'reply',
                'content': delta.content,
            }
