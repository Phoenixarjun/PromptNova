import asyncio
from typing import Any
from src.models.evaluateSchema import EvaluatePipelineInput, FullEvaluationResult
from src.agents.evaluate.llm_as_judge_agent import LLMAsJudgeAgent
from src.agents.evaluate.t_rag_agent import TRAGAgent
from src.agents.evaluate.mar_framework_agent import MARFrameworkAgent
from src.agents.evaluate.final_evaluate_agent import FinalEvaluateAgent
from src.logger import logger

class EvaluatePipeline:
    """A pipeline to evaluate a prompt using multiple frameworks concurrently."""

    def __init__(self, llm: Any):
        self.llm_as_judge_agent = LLMAsJudgeAgent(llm)
        self.t_rag_agent = TRAGAgent(llm)
        self.mar_framework_agent = MARFrameworkAgent(llm)
        self.final_evaluate_agent = FinalEvaluateAgent(llm)

    async def run(self, input_data: EvaluatePipelineInput) -> FullEvaluationResult:
        """
        Runs the full prompt evaluation pipeline asynchronously.
        """
        prompt = input_data.prompt_to_evaluate
        initial_prompt = input_data.initial_prompt

        logger.info("--- Starting Prompt Evaluation Pipeline ---")

        # Run evaluation agents concurrently
        evaluation_tasks = [
            self.llm_as_judge_agent.evaluate(prompt),
            self.t_rag_agent.evaluate(prompt, initial_prompt=initial_prompt),
            self.mar_framework_agent.evaluate(prompt),
        ]

        results = await asyncio.gather(*evaluation_tasks, return_exceptions=True)
        
        # Unpack results and handle potential errors
        llm_as_judge_result, t_rag_result, mar_result = results

        if any(isinstance(res, Exception) for res in results):
            logger.error(f"An error occurred during parallel evaluation: {results}")
            # Handle or raise the exception as needed
            raise Exception("One or more evaluation agents failed.")

        logger.info(f"LLM-as-a-Judge Result: {llm_as_judge_result}")
        logger.info(f"T-RAG Result: {t_rag_result}")
        logger.info(f"MAR Framework Result: {mar_result}")

        logger.info("\n--- Individual Evaluations Complete. Synthesizing Final Report... ---")

        final_evaluation = await self.final_evaluate_agent.evaluate(
            prompt_to_evaluate=prompt,
            llm_as_judge_result=llm_as_judge_result,
            t_rag_result=t_rag_result,
            mar_result=mar_result,
        )

        logger.info("\n--- Pipeline Finished ---")
        logger.info(f"Final Evaluation Result: {final_evaluation}")

        return FullEvaluationResult(
            llm_as_judge=llm_as_judge_result,
            t_rag=t_rag_result,
            mar_framework=mar_result,
            final_evaluation=final_evaluation,
        )
