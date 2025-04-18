from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def create_agent():
    agent = Agent(
        name = "Temporary Chat Replying Agent",
        model=Gemini(id="gemini-2.0-flash", api_key= os.getenv("GOOGLE_API_KEY")),
        instructions= [
            "You're a translation agent, your job is to translate an english content to hindi written content always.",
            "No other languages should be entertained. Only English to Hindi word shall be done."
        ],
        markdown=True,
        add_history_to_messages= True,
        num_history_responses= 10
    )
    return agent

def get_response(agent, content):

    response: RunResponse = agent.run(f"User Message:{content}, Now give translated to hindi sentence")
    return response.content

if __name__ == "__main__":
    agent = create_agent()
    while True:
        user = input("User Input: ")
        print(f"Agent:\n{get_response(agent,user)}")


