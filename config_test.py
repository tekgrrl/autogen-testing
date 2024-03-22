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

print(config_list)