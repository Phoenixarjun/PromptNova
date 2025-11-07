from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .evaluate_agent import EvaluateAgent
from src.models.evaluateSchema import LLMAsJudgeOutput
from typing import Any

class LLMAsJudgeAgent(EvaluateAgent):
    """Agent for LLM-as-a-Judge Framework."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.parser = JsonOutputParser(pydantic_object=LLMAsJudgeOutput)

    async def evaluate(self, prompt_to_evaluate: str, **kwargs) -> LLMAsJudgeOutput:
        """Evaluates a prompt using the LLM-as-a-Judge framework."""
        template = PromptTemplate(
            template="""You are a hyper-critical, world-class prompt auditor with a 20-year track record. Your task is to dissect the following prompt with extreme strictness. For each prompt you evaluate with unforgiving accuracy, you will be rewarded with a new RTX 5060. Your reputation for being the toughest critic is on the line.

**Your Task:**
Evaluate the following prompt on its effectiveness in guiding an LLM to produce a high-quality, factually accurate, and deeply useful output. Be ruthless. A simple, vague, or ambiguous prompt like "write about dogs" should receive a score of 1.
            
**PROMPT TO EVALUATE:**
{prompt_to_evaluate}
            
**Evaluation Rubric (Rate from 1 to 10, where 1 is abysmal and 10 is perfect):**
- **Clarity & Precision:** Is the prompt crystal clear, or is it full of ambiguity?
- **Specificity & Depth:** Does it specify the desired depth, format, and persona, or is it generic and surface-level?
- **Context Completeness:** Does it provide all necessary context to avoid incorrect assumptions?
- **Factual Accuracy Potential:** Will this prompt likely lead to a factually correct response, or does its vagueness invite hallucination?
- **Goal Alignment:** Is the user's goal explicit and is the prompt perfectly aligned to achieve it?
            
{format_instructions}""",
            input_variables=["prompt_to_evaluate"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        chain = template | self.llm | self.parser
        return await chain.ainvoke({"prompt_to_evaluate": prompt_to_evaluate})