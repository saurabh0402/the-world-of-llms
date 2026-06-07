from openai import OpenAI

client = OpenAI(
   base_url='http://localhost:8080/v1',
    api_key='dummy',
)

current_stream = {
    'stream': None
}

def generate_response(audio):
    stream = client.chat.completions.create(
        model='models/gemma-4-E4B-it-Q4_K_M.gguf',
        messages=[
            {
                'role': 'system',
                'content': [{
                    'type': 'text',
                    'text': '''
                        You are a helpful audio assistant, user is going to ask you some question and your
                        aim is to answer the question as succintly and acuurately as possible.
                    ''',
                }]
            },
            {
                'role': 'user',
                'content': [{
                    'type': 'input_audio',
                    'input_audio': {
                        'data': f'{audio}',
                        'format': 'wav',
                    }
                }]
            }
        ],
        stream=True
    )

    current_stream['stream'] = stream
    thinking = False

    try:
        for chunk in stream:
            delta = chunk.choices[0].delta

            if getattr(delta, "reasoning_content", None):
                if not thinking:
                    print(f'🤔 Thinking how to answer your question')
                    print('-----------------------------------------------------------------------------')

                thinking = True
                print(f'\033[2m{delta.reasoning_content}\033[0m', end="", flush=True)

            if delta.content:
                if thinking:
                    thinking = False
                    print('\n-----------------------------------------------------------------------------')

                yield delta.content
    except:
        pass
    finally:
        current_stream['stream'] = None
        
def stop_generation():
    stream = current_stream['stream']
    if stream:
        stream.close()
