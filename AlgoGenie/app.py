import streamlit as st
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container,stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio




st.title("AlgoGenie -  DSA Problem Solver")
st.write("Welcome to AlgoGenie, your personal DSA problem solver! Here you can ask solutions to various data structures and algorithms problems.")

task = st.text_input("Enter your DSA problem or question:",value='Write a function to add two numbers')

async def run(team,docker,task):
    try:
        await start_docker_container(docker)
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print(msg:= f"{message.source} : {message.content}")
                yield msg
            elif isinstance(message, TaskResult):
                print(msg:= f"Stop Reason: {message.stop_reason}")
                yield msg
        print("Task Completed")
    except Exception as e:
        print(f"Error: {e}")
        yield f"Error: {e}"
    finally:
        await stop_docker_container(docker)


if st.button("Run"):
    st.write("Running the Task..")

    team,docker = get_dsa_team_and_docker()

    async def collect_messages():
        async for msg in run(team,docker,task):
            if isinstance(msg, str):
                if msg.startswith("user"):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(msg)
                elif msg.startswith('DSA_Problem_Solver_Agent'):
                    with st.chat_message('assistant',avatar='🧑‍💻'):
                        st.markdown(msg)
                elif msg.startswith('CodeExecutorAgent'):
                    with st.chat_message('assistant',avatar='🤖'):
                        st.markdown(msg)
            elif isinstance(msg, TaskResult):
                with st.chat_message('stopper',avatar='🚫'):
                    st.markdown(f"Task Completed: {msg.result}")
    
    asyncio.run(collect_messages())
            
