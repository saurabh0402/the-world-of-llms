from helpers.react import run_agent
from langchain.messages import HumanMessage

def main():
    while True:
        print("\n>>> ", end="")
        user_prompt = input()
        run_agent(user_prompt)

if __name__ == '__main__':
    main()
