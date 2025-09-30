#!/usr/bin/env python
import os
import google.generativeai as genai
from typing import Optional, List, Dict
from dotenv import load_dotenv
from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router

from .crews.generate_plan_crew.generate_plan_crew import GeneratePlanCrew
from .crews.review_plan_crew.review_plan_crew import ReviewPlanCrew

class BusinessPlanState(BaseModel):
    user_inputs: Dict = {}
    business_plan: str = ""
    #feedback: Optional[str] = None
    #valid: bool = False
    #retry_count: int = 0

class BusinessPlanFlow(Flow[BusinessPlanState]):
    @start("done")
    async def generate_business_plan(self):
        crew = GeneratePlanCrew()
        result = crew.run(inputs=self.state.user_inputs)
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
