from langchain.prompts import PromptTemplate
from typing import Any

class PickAgent:
    """Agent that intelligently selects prompt types and framework based on user input."""

    def __init__(self, llm: Any):
        self.llm = llm

    def pick(self, user_input: str) -> str:
        """Selects the most suitable prompt types and framework based on user input."""
        pick_template = PromptTemplate(
            input_variables=["user_input"],
            template="""You are a world-class prompt engineer with 20+ years of expertise in all advanced prompting methods and frameworks.

Your goal is to analyze the given user input and select the most suitable combination of:
- **Prompt Types** (up to 4 or 5 only, no more)
- **Framework** (exactly one)

Available Prompt Types:
Zero Shot, One Shot, Chain of Thought (CoT), Tree of Thought (ToT), ReAct, In Context, Role, Few Shot, Self Consistency, Meta Prompting, Least to Most, Multi Task, Task Decomposition, Constrained, Generated Knowledge, Automatic Prompt Engineering, Directional Stimulus, Chain-of-Verification (CoVe), Skeleton-of-Thought (SoT), Graph-of-Thoughts (GoT), Plan-and-Solve (PS), Maieutic Prompting, Reflexion, Chain-of-Density (CoD), Active-Prompt, Retrieval-Augmented (RAP), Multi-Agent Debate, Emotion, Persona Switching, Scaffolded Prompting, Deliberation Prompting, Context Expansion, Goal-Oriented Prompting.

Available Frameworks:
Co-Star, TCEF, CRISPE, ICE, CRAFT, APE, PECRA, OSCAR, RASCE, Reflection, Flipped Interaction, BAB, PROMPT Framework, CLEAR, PRISM, GRIPS, APP, SOAP, SCOPE, Tool-Oriented Prompting (TOP), Neuro-Symbolic Prompting, Dynamic Context Windows, Meta-Cognitive Prompting, Prompt Ensembles.

**Instructions:**
1. Understand the intent behind the user's input (e.g., writing, coding, reasoning, creative, analytical, planning).
2. Choose only the most relevant 3–5 prompt types that would yield the best results.
3. Pick exactly one framework that complements those types and aligns with the task domain.
4. Output a strict JSON object with this exact structure:

{{
  "types": ["type1", "type2", "type3"],
  "framework": "framework_name"
}}

Ensure:
- Types are lowercase with underscores instead of spaces or special characters (e.g., "chain_of_thought", "task_decomposition").
- Framework is lowercase with underscores (e.g., "co_star").
- Output **only** the JSON, no explanations or extra text.

User Input: {user_input}
"""
        )

        chain = pick_template | self.llm
        return chain.invoke({"user_input": user_input}).content
