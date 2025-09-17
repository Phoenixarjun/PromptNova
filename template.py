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
    f"src/agents/final_prompt.py",
    f"src/agents/refine_agent.py",
    f"src/agents/self_correction.py",

    f"src/agents/types/zero_shot.py",
    f"src/agents/types/one_shot.py",
    f"src/agents/types/chain_of_thought.py",
    f"src/agents/types/tree_of_thought.py",
    f"src/agents/types/react.py",
    f"src/agents/types/in_context.py",
    f"src/agents/types/emotion.py",
    f"src/agents/types/role.py",
    f"src/agents/types/few_shot.py",
    f"src/agents/types/self_consistency.py",
    f"src/agents/types/meta_prompting.py",
    f"src/agents/types/least_to_most.py",
    f"src/agents/types/multi_task.py",
    f"src/agents/types/task_decomposition.py",
    f"src/agents/types/constrained.py",
    f"src/agents/types/generated_knowledge.py",
    f"src/agents/types/automatic_prompt_engineering.py",
    f"src/agents/types/directional_stimulus.py",
    f"src/agents/types/chain_of_verification.py",
    f"src/agents/types/skeleton_of_thought.py",
    f"src/agents/types/graph_of_thoughts.py",
    f"src/agents/types/plan_and_solve.py",
    f"src/agents/types/maieutic_prompting.py",
    f"src/agents/types/reflexion.py",
    f"src/agents/types/chain_of_density.py",
    f"src/agents/types/active_prompt.py",
    f"src/agents/types/retrieval_augmented_prompting.py",
    f"src/agents/types/multi_agent_debate.py",
    f"src/agents/types/persona_switching.py",
    f"src/agents/types/scaffolded_prompting.py",
    f"src/agents/types/deliberation_prompting.py",
    f"src/agents/types/context_expansion.py",
    f"src/agents/types/goal_oriented_prompting.py",

    f"src/agents/frameworks/co_star.py",
    f"src/agents/frameworks/tcef.py",
    f"src/agents/frameworks/crispe.py",
    f"src/agents/frameworks/rtf.py",
    f"src/agents/frameworks/ice.py",
    f"src/agents/frameworks/craft.py",
    f"src/agents/frameworks/ape.py",
    f"src/agents/frameworks/pecra.py",
    f"src/agents/frameworks/oscar.py",
    f"src/agents/frameworks/rasce.py",
    f"src/agents/frameworks/reflection.py",
    f"src/agents/frameworks/flipped_interaction.py",
    f"src/agents/frameworks/bab.py",
    f"src/agents/frameworks/prompt_framework.py",
    f"src/agents/frameworks/soap.py",
    f"src/agents/frameworks/clear.py",
    f"src/agents/frameworks/prism.py",
    f"src/agents/frameworks/grips.py",
    f"src/agents/frameworks/app_framework.py",
    f"src/agents/frameworks/scope.py",
    f"src/agents/frameworks/tool_oriented_prompting.py",
    f"src/agents/frameworks/neuro_symbolic_prompting.py",
    f"src/agents/frameworks/dynamic_context_windows.py",
    f"src/agents/frameworks/meta_cognitive_prompting.py",
    f"src/agents/frameworks/prompt_ensembles.py",

    f"src/chains/pipeline.py",

    f"src/models/prompt_schema.py",
    f"src/models/typeSchema.py",
    f"src/models/frameworkSchema.py",

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