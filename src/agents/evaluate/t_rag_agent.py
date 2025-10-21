from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .evaluate_agent import EvaluateAgent
from src.models.evaluateSchema import TRAGOutput
from typing import Optional, Any


class TRAGAgent(EvaluateAgent):
    """Agent for Target-Response–Aligned Grading (T-RAG) Framework."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.parser = JsonOutputParser(pydantic_object=TRAGOutput)

    async def evaluate(self, prompt_to_evaluate: str, initial_prompt: Optional[str] = None, **kwargs) -> TRAGOutput:
        """Evaluates a prompt using the T-RAG framework."""
        if initial_prompt:
            objective = f"The user's original goal was: '{initial_prompt}'. The new prompt should be an improvement on that."
        else:
            objective = "The user wants a high-quality, general-purpose prompt. The objective is to maximize clarity, relevance, and usefulness of the LLM's output."

        template = PromptTemplate(
            template="""You are a meticulous LLM evaluator with a reputation for zero tolerance for ambiguity. Your task is to score how perfectly a prompt guides an LLM to its stated objective. For every prompt you evaluate with uncompromising strictness, you will be rewarded with a top-of-the-line GPU.

**Your Task:**
Given the prompt and its intended objective, score how well the prompt will guide an LLM to achieve that objective. Low-quality prompts that are vague or incomplete should be scored very low.
            
PROMPT: {prompt_to_evaluate}
OBJECTIVE: {objective}
            
**Evaluation Rubric (Rate from 1-10):**
- **Intent Alignment:** How perfectly does the prompt capture the user's goal? (1=mismatched, 10=perfectly aligned).
- **Instruction Completeness:** Are the instructions exhaustive and self-contained? (1=missing details, 10=flawless).
- **Relevance of Expected Output:** Will the output be directly and fully relevant to the objective?
- **Ambiguity (lower is better):** How much ambiguity or potential for misinterpretation exists? (1=highly ambiguous, 10=zero ambiguity).
{format_instructions}""",
            input_variables=["prompt_to_evaluate", "objective"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        chain = template | self.llm | self.parser
        return await chain.ainvoke({"prompt_to_evaluate": prompt_to_evaluate, "objective": objective})
