import requests

#Ultimetly this would be in front end and server would be running on the backend


def main():
    import sys
    import os
    
    # Add the project root directory to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, project_root)
    
    from agent.MCPLangChainServer import (
       
        agent
    )

    # Check if agent is properly initialized
    if agent is None:
        print("Error: Agent is not initialized. Please check your OpenAI API key configuration.")
        return

    user_input = input("Enter a question: ")
    
    while user_input != "exit":
        try:
            # Agent response is a dictionary, not a requests response
            res = agent.invoke({"input": user_input})
            
            # Extract the output from the agent response
            if isinstance(res, dict) and "output" in res:
                print(res["output"])
            else:
                print(str(res))
        except Exception as e:
            print(f"Error: {str(e)}")

        user_input = input("Enter a question: ")

if __name__ == "__main__":
    main()
