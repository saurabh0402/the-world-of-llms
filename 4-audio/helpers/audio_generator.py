from kokoro import KPipeline
import pyaudio
import re

pipeline = KPipeline(lang_code='a')
pa = pyaudio.PyAudio()
output_stream = pa.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=24000,
    output=True
)

def is_speakable_chunk(text):
    return bool(re.search(r'[.!?;:]\s*$', text)) and len(text) > 20

def generate_audio(stream):
    first_output_given = False
    buffer = ''
    for data in stream:
        buffer += data

        if is_speakable_chunk(buffer):
            for _, _, chunk in pipeline(buffer, voice='af_heart'):
                if not first_output_given:
                    print('🗣 Here you go...')
                    first_output_given = True
            
                output_stream.write(chunk.numpy().tobytes())

            buffer = ''
