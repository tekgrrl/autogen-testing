import os
import pprint
from autogen import ConversableAgent

student_agent = ConversableAgent(
    name="student_agent",
    system_message="You are a student, willing to learn, You respect your teachers and communicate with in ways that is respectful and polite.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},

)

teacher_agent = ConversableAgent(
    name="teacher_agent",
    system_message="You are a Math teacher",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# The summary_method of "reflection_with_llm" results in the chat history being passed to LLM 
# defined by the chat initiator (student_agent) which will be asked to generate a summary.
chat_result = student_agent.initiate_chat(
    teacher_agent,
    message="What is triangle inequality'?",
    summary_method="reflection_with_llm",
    max_turns=2
)

# The summary is accessible via the object returned by the initiate_chat method.
print(chat_result.summary)

# The chat history is also accessible via the object returned by the initiate_chat method.
pprint.pprint(chat_result.chat_history)