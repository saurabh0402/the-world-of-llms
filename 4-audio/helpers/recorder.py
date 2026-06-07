import collections
import wave
import numpy as np
import webrtcvad
import base64
import os
import pyaudio
import io

FORMAT = pyaudio.paInt16
CHANNELS = 1
FRAME_DURATION_MS = 30
VAD_AGGRESSIVENESS = 3
SILENCE_TIMEOUT_SEC = 3.0
NUM_SILENCE_FRAMES = int(SILENCE_TIMEOUT_SEC * 1000 / FRAME_DURATION_MS)

def get_input_devices():
    input_devices = []
    pa = pyaudio.PyAudio()

    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            input_devices.append((i, info['name']))

    return input_devices

def get_ip_device_from_user():
    ip_devices = get_input_devices()

    if not ip_devices:
        print('😔 No Input device found')
        exit(None, None)

    print('Choose Input Device:')
    for ip_device in ip_devices:
        print(f'    {ip_device[0]} {ip_device[1]}')

    ip_device_index = int(input('Enter an index: '))
    selected_device = None
    for ip_device in ip_devices:
        if ip_device[0] == ip_device_index:
            selected_device = ip_device
            break

    if not selected_device:
        print('😡 Invalid device selected')
        exit()

    return selected_device

def record(device_index):
    pa = pyaudio.PyAudio()
    vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)

    supported_rates = [48000, 32000, 16000, 8000]
    selected_rate = -1
    for rate in supported_rates:
        try:
            if pa.is_format_supported(
                rate,
                input_device=device_index,
                input_channels=CHANNELS,
                input_format=FORMAT
            ):
                selected_rate = rate
                break
        except:
            pass

    if selected_rate == -1:
        raise Exception('No rate supported')

    chunk = int(selected_rate * FRAME_DURATION_MS / 1000)

    stream = pa.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=selected_rate,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=chunk,
    )

    audio_frames = []
    has_spoken = False
    silence_buffer = collections.deque(maxlen=NUM_SILENCE_FRAMES)

    while True:
        frame_data = stream.read(chunk, exception_on_overflow=False)
        is_speech = vad.is_speech(frame_data, selected_rate)

        if not has_spoken:
            if is_speech:
                print('👂 Keep speaking, I am all ears')
                has_spoken = True
                audio_frames.append(frame_data)
        else:
            if is_speech:
                audio_frames.append(frame_data)
                silence_buffer.append(0)
            else:
                silence_buffer.append(1)

            if (
                has_spoken and
                len(silence_buffer) == NUM_SILENCE_FRAMES and
                sum(silence_buffer) == NUM_SILENCE_FRAMES
            ):
                print('🤖 Now that you have spoken, I will start processing')
                break

    stream.stop_stream()
    stream.close()
    pa.terminate()

    if audio_frames:
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pa.get_sample_size(FORMAT))
            wf.setframerate(selected_rate)
            wf.writeframes(b"".join(audio_frames))
    
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    else:
        return None
