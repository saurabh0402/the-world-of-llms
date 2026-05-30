from openai import OpenAI
import base64

client = OpenAI(
    base_url='http://localhost:8080/v1',
    api_key='dummy',
)

def main():
    with open('./us.jpg', 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')

        stream = client.chat.completions.create(
            model='models/gemma-4-E4B-it-Q4_K_M.gguf',
            messages=[
                {
                    'role': 'user',
                    'content': [{
                        'type': 'text',
                        'text': 'Tell me about the country whose map is represented in the image'
                    }, {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/webp;base64,{encoded_image}'
                        }
                    }]
                }
            ],
            stream=True
        )

        thinking = False

        for chunk in stream:
            delta = chunk.choices[0].delta

            if getattr(delta, "reasoning_content", None):
                thinking = True
                print(f'\033[2m{delta.reasoning_content}\033[0m', end="", flush=True)

            if delta.content:
                if thinking:
                    thinking = False
                    print('\n')
                print(delta.content, end="", flush=True)

if __name__ == '__main__':
    main()
