import tempfile
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import ConversableAgent


# Create a temporary directory to store the generated code
temp_dir = tempfile.TemporaryDirectory(delete=False)
print(temp_dir.name)

# Create local command line code executor
executor = LocalCommandLineCodeExecutor(
    timeout=10,
    work_dir=temp_dir.name,
)

print(type(executor.work_dir))

# Create an agent with code executor configuration.
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

# Cooment out the following two lines to run a basic test of code execution
reply = code_executor_agent.generate_reply(messages=[{"role": "user", "content": message_with_code_block}])
print(reply)