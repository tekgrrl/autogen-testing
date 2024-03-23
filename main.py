import os
import json
import autogen
import tempfile
from pathlib import Path
from autogen import runtime_logging


# Setting configurations for autogen
config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-4",
            "gpt4",
            "gpt-4-0125-preview",
            "gpt-4-1106-preview",
            "gpt-4-32k",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0125",
            "mixtral",
            "llama2",
            "codellama",
        }
    }
)

gpt4_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

logging_session_id = runtime_logging.start(config={"dbname": "logs.db"})

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt4_config,
    system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
""",
    description="An engineer that follows an approved plan and writes Python code or shell scripts to solve tasks.",
)
scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=gpt4_config,
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""",
    description="A scientist that follows an approved plan and categorizes papers based on their abstracts. They do not write code.",
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
""",
    llm_config=gpt4_config,
    description="A planner that suggests a plan and revises it based on feedback until it is approved by the admin.",
)
executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    description="Someone that can execute Python code or shell scripts and then report the results.",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "paper",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=gpt4_config,
    description="A critic that double checks plans, claims, and code from other agents and provides feedback.",
)
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=50
)
manager = autogen.GroupChatManager(
    groupchat=groupchat, 
    llm_config=gpt4_config
)

user_proxy.initiate_chat(
    manager,
    message="""
        Find papers on LLM applications from arxiv in the last day using its API, create a markdown table of different domains.
    """,
)

runtime_logging.stop()


def get_log(dbname="logs.db", table="chat_completions"):
    import sqlite3
    import json

    con = sqlite3.connect(dbname)
    query = f"SELECT * from {table}"
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    print(column_names)
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()

    json_data = json.dumps(data,
                           indent=6,
                           )


    return json_data

logs = get_log()
temp_file = tempfile.NamedTemporaryFile(
    dir="logs",
    delete=False,
    mode="w",
    suffix=".log"
)

temp_file.write(logs)

temp_file.close()