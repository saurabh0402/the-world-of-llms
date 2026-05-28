from helpers.react import run_agent
from langchain.messages import HumanMessage
import signal
import sys

def exit(sig, frame):
    print('\nBye 👋')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, exit)

    while True:
        try:
            print("\n>>> ", end="")
            user_prompt = input()
            run_agent(user_prompt)
        except KeyboardInterrupt:
            exit(None, None)

if __name__ == '__main__':
    main()
