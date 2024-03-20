import tempfile
import os
from autogen import ConversableAgent, runtime_logging
from autogen.coding import LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor

# Start logging. Note that logging is not compatible with LocalCommandLineCodeExecutor
# because it has non-serializable objects in its configuration.
logging_session_id = runtime_logging.start(config={"dbname": "logs.db"})
print("Logging session ID: " + str(logging_session_id))

agent_with_number = ConversableAgent(
    "agent_with_number",
    system_message="You are playing a game of guess-my-number. "
    "In the first game, you have the "
    "number 53 in your mind, and I will try to guess it. "
    "If I guess too high, say 'too high', if I guess too low, say 'too low'. ",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    max_consecutive_auto_reply=1,  # maximum number of consecutive auto-replies before asking for human input
    is_termination_msg=lambda msg: "53" in msg["content"],  # terminate if the number is guessed by the other agent
    human_input_mode="TERMINATE",  # ask for human input until the game is terminated
)

agent_guess_number = ConversableAgent(
    "agent_guess_number",
    system_message="I have a number in my mind, and you will try to guess it. "
    "If I say 'too high', you should guess a lower number. If I say 'too low', "
    "you should guess a higher number. ",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="NEVER",
)

result = agent_with_number.initiate_chat(
    agent_guess_number,
    message="I have a number between 52 and 54. Guess it!",
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

    json_data = json.dumps(data)

    return json_data

logs = get_log()
print(logs)
