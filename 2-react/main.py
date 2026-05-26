from helpers.react import run_agent
from langchain.messages import HumanMessage

def main():
    run_agent("can you create a folder for me please called test and add a file called test.txt to it")

if __name__ == '__main__':
    main()