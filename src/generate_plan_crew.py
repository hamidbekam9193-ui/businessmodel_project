# --- START OF FILE src/generate_plan_crew.py ---

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
import os
# from dotenv import load_dotenv # No longer needed here
# from pathlib import Path # No longer needed here

# Remove the load_env_from_project_root function and its call
# The .env loading is now handled in backend.py at the entry point.

@CrewBase
class GeneratePlanCrew():
    """GeneratePlanCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, gemini_api_key: str, groq_api_key: str):
        """
        Constructor to accept API keys dynamically.
        These keys are passed from src/main.py, which received them from backend.py.
        """
        self._gemini_api_key = gemini_api_key
        self._groq_api_key = groq_api_key
        # Initialize LLM attributes to None so properties can lazy-load them
        self._llm_gemini = None
        self._llm_groq = None

    @property
    def llm_gemini(self):
        if not self._llm_gemini: # Check if already initialized
            if not self._gemini_api_key:
                raise ValueError("Gemini API key not provided to GeneratePlanCrew.")
            import google.generativeai as genai
            genai.configure(api_key=self._gemini_api_key)

            self._llm_gemini = LLM(
                model="gemini/gemini-2.5-pro-preview-05-06",
                temperature=0.1,
                reasoning_effort="high"
            )
        return self._llm_gemini

    @property
    def llm_groq(self):
        if not self._llm_groq: # Check if already initialized
            if not self._groq_api_key:
                raise ValueError("Groq API key not provided to GeneratePlanCrew.")
            # For Groq, the API key can be set via an environment variable
            # or passed directly to the client. CrewAI's LLM wrapper handles this
            # by looking at the GROQ_API_KEY environment variable.
            # So, we temporarily set it here before LLM initialization if it's not already set
            # or if we want to ensure the dynamic key is used.
            # A cleaner way is to ensure CrewAI's Groq LLM uses it when passed as argument.
            # Let's ensure it's set in the environment for the LLM to pick it up.
            # Or, if CrewAI LLM supports passing it directly:
            # from crewai_tools.llms import Groq  # Example if using crewai-tools
            # self._llm_groq = Groq(groq_api_key=self._groq_api_key, model_name="llama-3.3-70b-versatile")

            # For the generic CrewAI LLM, it usually expects env vars.
            # Set the environment variable just for this context if not already set.
            original_groq_api_key = os.environ.get("GROQ_API_KEY")
            if original_groq_api_key != self._groq_api_key:
                 os.environ["GROQ_API_KEY"] = self._groq_api_key

            self._llm_groq = LLM(
                model="groq/llama-3.3-70b-versatile",
                temperature=0.1,
                reasoning_effort="medium"
            )
            # Restore original if changed for this instance
            if original_groq_api_key != self._groq_api_key:
                if original_groq_api_key is not None:
                    os.environ["GROQ_API_KEY"] = original_groq_api_key
                else:
                    del os.environ["GROQ_API_KEY"] # Clean up if it wasn't there before

        return self._llm_groq

    @before_kickoff
    def before_kickoff_function(self, inputs):
        # inputs here will contain the user-provided form data, but NOT the API keys
        # as they were handled in the __init__ of GeneratePlanCrew.
        return inputs

    @agent
    def business_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['business_designer'],
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini, # Use the property to get the configured LLM
            verbose=True
        )

    @agent
    def product_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['product_designer'],
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['market_analyst'],
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def marketing_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['marketing_expert'],
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def operations_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['operations_specialist'],
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def financial_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_expert'],
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def consolidator(self) -> Agent:
        return Agent(
            config=self.agents_config['consolidator'],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config['evaluator'],
            llm=self.llm_groq, # Use the property to get the configured LLM
            verbose=True
        )

    @agent
    def refiner(self) -> Agent:
        return Agent(
            config=self.agents_config['refiner'],
            llm=self.llm_groq,
            verbose=True
        )

    @task
    def create_business_concept(self) -> Task:
        return Task(
            config=self.tasks_config['create_business_concept']
        )

    @task
    def create_product_design(self) -> Task:
        return Task(
            config=self.tasks_config['create_product_design'],
            context=[self.create_business_concept()]
        )

    @task
    def create_market_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['create_market_analysis'],
            context=[self.create_business_concept(), self.create_product_design()]
        )

    @task
    def create_marketing_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_marketing_plan'],
            context=[self.create_business_concept(), self.create_product_design(), self.create_market_analysis()]
        )

    @task
    def create_operating_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_operating_plan'],
            context=[self.create_business_concept(), self.create_product_design(), self.create_market_analysis(), self.create_marketing_plan()]
        )

    @task
    def create_financial_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_financial_plan'],
            context=[self.create_business_concept(), self.create_product_design(), self.create_market_analysis(), self.create_marketing_plan(), self.create_operating_plan()]
        )

    @task
    def consolidate_plan(self) -> Task:
        return Task(
            config=self.tasks_config['consolidate_plan'],
            context=[self.create_business_concept(), self.create_product_design(), self.create_market_analysis(), self.create_marketing_plan(), self.create_operating_plan(), self.create_financial_plan()]
        )

    @task
    def evaluate_plan(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_plan'],
            context=[self.consolidate_plan()]
        )

    @task
    def refine_plan(self) -> Task:
        return Task(
            config=self.tasks_config['refine_plan'],
            context=[self.consolidate_plan(), self.evaluate_plan()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GeneratePlanCrew crew"""
        # Ensure LLMs are initialized by accessing their properties
        _ = self.llm_gemini
        _ = self.llm_groq

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def run(self, inputs: dict = None):
        try:
            result = self.crew().kickoff(inputs=inputs)
            return result
        except Exception as e:
            raise Exception(f"Error while running the crew: {e}")
