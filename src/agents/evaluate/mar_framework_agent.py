from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .evaluate_agent import EvaluateAgent
from src.models.evaluateSchema import MARFrameworkOutput
from typing import Any

class MARFrameworkAgent(EvaluateAgent):
    """Agent for Multi-Aspect Rubric (MAR) Framework."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.parser = JsonOutputParser(pydantic_object=MARFrameworkOutput)

    async def evaluate(self, prompt_to_evaluate: str, **kwargs) -> MARFrameworkOutput:
        """Evaluates a prompt using the MAR framework."""
        template = PromptTemplate(
            template="""You are a senior prompt auditor known for your rigorous, quantitative analysis. Your evaluations are trusted by top AI labs. For each strict and accurate evaluation, you earn a significant bonus.

**Your Task:**
Evaluate the quality of the following prompt using this weighted rubric. Be demanding. A simple or poorly-defined prompt should not score high on any dimension.
            
**PROMPT TO EVALUATE:**
{prompt_to_evaluate}

**Rubric (Scores from 1-10 for each):**
1. **Clarity & Unambiguity (20%):** Is every part of the prompt clear and free of jargon?
2. **Completeness & Context (20%):** Does the prompt contain all necessary information and context?
3. **Relevance & Factual Grounding (20%):** Is the prompt directly relevant to a clear goal and likely to produce factually sound output?
4. **Structure & Constraints (20%):** Does the prompt define a clear structure, format, and constraints for the output?
5. **Creativity / Precision Balance (20%):** Does the prompt strike the right balance, allowing for creativity where needed but demanding precision where it matters?
{format_instructions}""",
            input_variables=["prompt_to_evaluate"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        chain = template | self.llm | self.parser
        return await chain.ainvoke({"prompt_to_evaluate": prompt_to_evaluate})
