import tempfile
import os
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor

# Create a temporary directory to store the generated code
temp_dir = tempfile.TemporaryDirectory()

# Creat local command line code executor
executor = LocalCommandLineCodeExecutor(
    timeout=10,
    work_dir=temp_dir.name
)

# Creat an agent with code executor configuration.
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor}, # Use the local command line code executor
    human_input_mode="ALWAYS",
)

message_with_code_block = """This is a message with code block.
The code block is below:
```python
import numpy as np
import matplotlib.pyplot as plt
x = np.random.randint(0, 100, 100)
y = np.random.randint(0, 100, 100)
plt.scatter(x, y)
plt.savefig('scatter.png')
print('Scatter plot saved to scatter.png')
```
This is the end of the message.
"""

# Generate a reply for the given code.
reply = code_executor_agent.generate_reply(messages=[{"role": "user", "content": message_with_code_block}])



# Create a docker command line code executor
docker_executor = DockerCommandLineCodeExecutor(
    timeout=10,
    work_dir=temp_dir.name,
    image="python:3.12-slim", # Execute the code in a python docker image
)

# Create an agent with code executor congiguration that uses Docker.
docker_code_executor_agent = ConversableAgent(
    "docker_code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": docker_executor}, # Use the docker command line code executor
    human_input_mode="ALWAYS",
)

docker_code_executor_agent.generate_reply(messages=[{"role": "user", "content": message_with_code_block}])

# We can see the output scatter.png and the code file generated by the agent.
print(os.listdir(temp_dir.name))

temp_dir.cleanup()