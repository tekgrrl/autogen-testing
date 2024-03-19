from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, runtime_logging
from autogen.coding import LocalCommandLineCodeExecutor

import autogen
import os
from pathlib import Path

from matplotlib import lines

# Start logging
# logging_session_id = runtime_logging.start(config={"dbname": "logs.db"})
# print("Logging session ID: " + str(logging_session_id))

llm_config = {
    "config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}],
}


cathy = ConversableAgent("cathy", 
                        system_message="Your name is Cathy and you are one member of a duo of comedians.",
                        llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ["OPENAI_API_KEY"]}]},
                        human_input_mode="NEVER",)

bob = ConversableAgent("bob", 
                        system_message="Your name is Bob and you are one member of a duo of comedians.",
                        llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ["OPENAI_API_KEY"]}]},
                        human_input_mode="NEVER",
                        is_termination_msg=lambda msg: "good bye" in msg["content"].lower(),
                        )


result = bob.initiate_chat(cathy, message="Cathy, tell me a joke and then say the words GOOD BYE.", max_turns=3)     

# runtime_logging.stop()

# def get_log(dbname="logs.db", table="chat_completions"):
#     import sqlite3

#     con = sqlite3.connect(dbname)
#     query = f"SELECT * from {table}"
#     cursor = con.execute(query)
#     rows = cursor.fetchall()
#     column_names = [description[0] for description in cursor.description]
#     print(column_names)
#     data = [dict(zip(column_names, row)) for row in rows]
#     con.close()
#     return data

# logs = get_log()

# with open("logs.txt", "w") as file:
#     for line in logs:
#         file.write(f"{line}\n")

