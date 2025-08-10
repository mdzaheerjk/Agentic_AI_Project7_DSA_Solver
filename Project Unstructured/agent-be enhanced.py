from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
from autogen_agentchat.base import TaskResult
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)


async def main():

    docker = DockerCommandLineCodeExecutor(
        work_dir='temp',
        timeout=120
    )

    code_executor_agent = CodeExecutorAgent(
        name='CodeExecutorAgent',
        code_executor=docker)



    problem_solver_agent = AssistantAgent(
        name="DSA_Problem_Solver_Agent",
        description="An agent that solves DSA problems",
        model_client=model_client,
        system_message="""
            You are a problem solver agent that is an expert in solving DSA problems.
            You will be working with code executor agent to execute code.
            You will be given a task and you should. 
            At the beginning of your response you have to specify your plan to solve the task.
            Then you should give the code in a code block.(Python)
            You should write code in a one code block at a time and then pass it to code executor agent to execute it.
            Make sure that we have atleast 3 test cases for the code you write.
            Once the code is executed and if the same has been done successfully, you have the results.
            You should explain the code execution result.
            After explaining, make sure to call agent Executor again to 
            you save the code in a file named `solution.py` by providing a Python code block.
            You should also make sure to call the code executor agent to run it and save the same. like this:
            code = '''
            def greet():
                print("Hello from the new file!")

            greet()
            '''
            with open("new_script.py", "w") as f:
                f.write(code)

            print("New script saved as new_script.py")


            In the end once the code is executed successfully, you have to say "STOP" to stop the conversation.
            """
    )

    termination_condition = TextMentionTermination("STOP")

    team = RoundRobinGroupChat(
        participants=[problem_solver_agent,code_executor_agent],
        termination_condition=termination_condition,
        max_turns=10
    )

    try:
        await docker.start()
        task = 'Write a Python code to add two numbers.'
        
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print('==' * 20)
                print(message.source, ":", message.content)
            elif isinstance(message,TaskResult):
                print('Stop Reason:',message.stop_reason)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # print("Stopping docker executor")
        await docker.stop()


if __name__ == "__main__":
    asyncio.run(main())