
import tempfile
from autogen import ConversableAgent
from autogen.coding import DockerCommandLineCodeExecutor

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

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


# Create a Docker command line code executor
# for this I created and built a local pynumpy image using the following Dockerfile:
# FROM python:3.12-slim
# RUN pip install numpy matplotlib
executor = DockerCommandLineCodeExecutor(
    image="pynumpy",  # Execute code using the local docker image
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
    
)

# Create an agent with code executor configuration that uses docker.
code_executor_agent_using_docker = ConversableAgent(
    "code_executor_agent_docker",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the docker command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)

docker_reply = code_executor_agent_using_docker.generate_reply(messages=[{"role": "user", "content": message_with_code_block}])
print(docker_reply)


