import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "promptnova"

list_of_files = [
    f"src/__init__.py",
    f"src/config.py",
    f"src/logging.py",


    f"src/agents/prompt_agent.py",
    f"src/agents/zero_shot.py",
    f"src/agents/one_shot.py",
    f"src/agents/chain_of_thought.py",
    f"src/agents/tree_of_thought.py",
    f"src/agents/react.py",
    f"src/agents/in_context.py",
    f"src/agents/emotion.py",
    f"src/agents/role.py",
    f"src/agents/few_shot.py",
    f"src/agents/self_consistency.py",
    f"src/agents/meta_prompting.py",
    f"src/agents/least_to_most.py",
    f"src/agents/multi_task.py",
    f"src/agents/task_decomposition.py",
    f"src/agents/constrained.py",
    f"src/agents/generated_knowledge.py",
    f"src/agents/automatic_prompt_engineering.py",
    f"src/agents/directional_stimulus.py",

    
    f"src/chains/pipeline.py",  
    f"src/models/prompt_schema.py",
    f"research/testing.ipynb",
    "requirements.txt",
    "setup.py",
    "app.py",
    ".env"
]

if __name__ == '__main__':
    for filepath in list_of_files:
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)

        if filedir:
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"Created directory: {filedir}")

        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            with open(filepath, "w") as f:
                pass
            logging.info(f"Created empty file: {filepath}")
        else:
            logging.info(f"{filename} already exists.")