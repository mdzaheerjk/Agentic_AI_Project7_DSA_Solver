import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)


assistant = AssistantAgent(
    name='Assistant',
    description="A helpful assistant that can write poetry.",
    model_client=model_client,
    system_message="You are a helpful assistant.",
)

user_proxy_agent = UserProxyAgent(
    name='UserProxy',
    description="A proxy agent that represents the user.",
    input_func=input
)

termination = TextMentionTermination('APPROVE')

# Create a team with the assistant and user proxy agent
team = RoundRobinGroupChat(
    participants=[assistant, user_proxy_agent],
    termination_condition=termination
)


stream = team.run_stream(task = 'Write a 4 line poem about the ocean')

async def main():
    await Console(stream)

if __name__ == "__main__":
    asyncio.run(main())