import autogen
import os
import json

# This was testing I did to find out how to get OAI_CONFIG_LIST to work
# Basically I now add an environment variable OAI_CONFIG_LIST with the path to the config list
# You assume that when using env_or_file="OAI_CONFIG_LIST" the code would first check to see if 
# it points to a file but it doesn't

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
)

config_list_from_env = autogen.config_list_from_dotenv()


# Setting configurations for autogen
filtered_config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-4",
            "gpt4",
            "gpt-4-0125-preview",
            "gpt-4-32k",
            "gpt-4-32k-0314",
            "gpt-4-32k-v0314",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-0301",
            "chatgpt-35-turbo-0301",
            "gpt-35-turbo-v0301",
            "gpt",
            "llama2-chat-7B",
        }
    }
)


# env_or_file="OAI_CONFIG_LIST"
# env_str = os.environ.get(env_or_file)

# if env_str is None:
#     print("No environment variable found")
#     exit(-1)
# else:
#     with open(env_str, "r") as file:
#                 json_str = file.read()

# print(json_str)

# config_list = json.loads(json_str)

# print(config_list)

gpt4_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

print(filtered_config_list)