import signal
import sys
from helpers.recorder import record, get_ip_device_from_user
from helpers.llm import generate_response, stop_generation
from helpers.audio_generator import generate_audio
import time
from pynput import keyboard

def exit(sig, frame):
    print('\n👋 Bye, Bye. Talk to you soon')
    sys.exit(0)

# Register hot keys
signal.signal(signal.SIGINT, exit)
hotkeys = keyboard.GlobalHotKeys({'<ctrl>+x': stop_generation})
hotkeys.start()

def main():
    print('-----------------------------------------------------------------------------')
    print('👋 Hi, there. Press Ctrl+C to exit, and Ctrl+X to stop LLM from generating a response.')
    selected_device = get_ip_device_from_user()
    print('-----------------------------------------------------------------------------')

    print('🕓 Starting conversation in 3 seconds')
    time.sleep(3);

    while True:
        print('############################################################################################################')
        print('🎙️ Say something beautiful')
        audio_b64encoded = record(selected_device[0])
        generate_audio(generate_response(audio_b64encoded))
        print('############################################################################################################')

if __name__ == '__main__':
    main()
