import code
import tempfile
import os

from autogen import ConversableAgent, GroupChatManager, GroupChat

temp_dir = tempfile.gettempdir()

arithmetic_agent = ConversableAgent(
    name="arithmetic_agent",
    llm_config=False,
    human_input_mode="ALWAYS",
    # This agent will always require human input in order to make sure that the code
    # is safe to run.
    code_execution_config={"use_docker": False, "work_dir:": temp_dir},
)

code_writer_agent = ConversableAgent(
    name="code_writer_agent",
    system_message="You are a code write. You write Pyhton script in Markdown code blocks.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="NEVER",
)

poetry_agent = ConversableAgent(
    name="poetry_agent",
    system_message="You are an AI poet.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="NEVER",
)

group_chat_with_intros = GroupChat(
    agents=[code_writer_agent, poetry_agent],
    max_round=10,
    messages=[],
    send_introductions=True,
)

group_chat_manager_with_intros = GroupChatManager(
    groupchat=group_chat_with_intros,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

nested_chats = [
    {
        "recipient": group_chat_manager_with_intros,
        "summary_method": "reflection_with_llm",
        "summary_prompt": "Summarize the sequence of operations used to turn " "the source number into target number.",
    },
    {
        "recipient": code_writer_agent,
        "message": "Write a Python script to verify the arithmetic operations is correct.",
        "summary_method": "reflection_with_llm",
    },
    {
        "recipient": poetry_agent,
        "message": "Write a poem about it.",
        "max_turns": 1,
        "summary_method": "last_msg",
    },
]

arithmetic_agent.register_nested_chats(
    nested_chats,
    # The trigger function is used to determine if the agent should start the nested chat
    # given the sender agent.
    # In this case, the arithmetic agent will not start the nested chats if the sender is
    # from the nested chats' recipient to avoid recursive calls.
    trigger=lambda sender: sender not in [group_chat_manager_with_intros, code_writer_agent, poetry_agent],
)