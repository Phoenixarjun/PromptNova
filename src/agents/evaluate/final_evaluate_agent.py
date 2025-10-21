from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .evaluate_agent import EvaluateAgent
from src.models.evaluateSchema import LLMAsJudgeOutput, TRAGOutput, MARFrameworkOutput, FinalEvaluationOutput
from typing import Any
import json

class FinalEvaluateAgent(EvaluateAgent):
    """Agent to synthesize results from all evaluation frameworks."""

    def __init__(self, llm: Any):
        super().__init__(llm)
        self.parser = JsonOutputParser(pydantic_object=FinalEvaluationOutput)

    async def evaluate(
        self,
        prompt_to_evaluate: str,
        llm_as_judge_result: LLMAsJudgeOutput,
        t_rag_result: TRAGOutput,
        mar_result: MARFrameworkOutput,
        **kwargs
    ) -> FinalEvaluationOutput:
        """Synthesizes reports into a final review."""
        template = PromptTemplate(
            template="""You are the final arbiter of prompt quality, a master analyst responsible for synthesizing reports from three hyper-critical evaluation agents. Your final verdict is the definitive score. Your reputation for delivering brutally honest, actionable feedback is legendary.
            
**PROMPT UNDER REVIEW:**
"{prompt_to_evaluate}"
            
**EVALUATION REPORTS FROM YOUR TEAM:**
1. LLM-as-a-Judge Framework Results: {llm_as_judge_result}
2. T-RAG Framework Results: {t_rag_result}
3. MAR Framework Results: {mar_result}
            
**YOUR FINAL TASK:**
1.  **Final Score:** Synthesize the 'overall' scores into a single, brutally honest `final_score` from 0-100. Do not be lenient.
2.  **Strengths:** Identify any genuine strengths (1-2 sentences). If there are none, say so.
3.  **Areas for Improvement:** Provide direct, no-nonsense, actionable advice for improvement (1-2 sentences).
4.  **Concise Report:** Summarize the key finding from each of the three evaluation frameworks in a brief report.
{format_instructions}""",
            input_variables=["prompt_to_evaluate", "llm_as_judge_result", "t_rag_result", "mar_result"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        chain = template | self.llm | self.parser
        return await chain.ainvoke({
            "prompt_to_evaluate": prompt_to_evaluate,
            "llm_as_judge_result": json.dumps(llm_as_judge_result),
            "t_rag_result": json.dumps(t_rag_result),
            "mar_result": json.dumps(mar_result),
        })
