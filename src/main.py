# --- START OF FILE src/main.py ---

#!/usr/bin/env python
import os
# from google import genai
from typing import Optional, List, Dict
from dotenv import load_dotenv # Still good for local testing, though Render uses its own env vars
from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router

from .generate_plan_crew import GeneratePlanCrew
# from .crews.review_plan_crew.review_plan_crew import ReviewPlanCrew

class BusinessPlanState(BaseModel):
    user_inputs: Dict = {}
    business_plan: str = ""
    #feedback: Optional[str] = None
    #valid: bool = False
    #retry_count: int = 0

class BusinessPlanFlow(Flow[BusinessPlanState]):
    @start("done")
    async def generate_business_plan(self):
        # Extract API keys from user_inputs
        gemini_api_key = self.state.user_inputs.get("gemini_api_key")
        groq_api_key = self.state.user_inputs.get("groq_api_key")

        if not gemini_api_key or not groq_api_key:
            raise ValueError("API keys for Gemini and Groq must be provided.")

        # Initialize GeneratePlanCrew with the API keys
        crew = GeneratePlanCrew(gemini_api_key=gemini_api_key, groq_api_key=groq_api_key)

        # Pass the full user_inputs (excluding the keys which are handled by the crew's __init__)
        # to the run method for task context
        # It's better to remove the API keys from the inputs dictionary before passing to `crew.run`
        # as the crew itself will use them for LLM initialization.
        crew_inputs = {k: v for k, v in self.state.user_inputs.items() if k not in ["gemini_api_key", "groq_api_key"]}

        result = crew.run(inputs=crew_inputs)
        self.state.business_plan = result
        return self.state

    @listen("done")
    def done(self):
        return self.state

    #@router(generate_business_plan)
    #def evaluate_business_plan(self):
    #    if self.state.retry_count == 1:
    #        return "completed"
    #    crew = ReviewPlanCrew()
    #    result = crew.run(input={"business_plan": "\n\n".join(self.state.business_plan)})
    #    self.state.feedback = result
    #    self.state.retry_count += 1

    #    return "retry"

    #@listen("completed")
    #def save_business_plan(self):
    #    return self.state

