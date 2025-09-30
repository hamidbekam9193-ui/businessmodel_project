from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
import os
from dotenv import load_dotenv

from .tools.CharacterCounterTool import CharacterCounterTool

from pathlib import Path

def load_env_from_project_root(env_filename=".env", max_depth=5) -> bool:
    """
    Recursively searches upward from the current file's path to find and load a .env file.

    Args:
        env_filename (str): Name of the env file to search for (default: ".env")
        max_depth (int): Max levels to go up the directory tree

    Returns:
        bool: True if the file was found and loaded, False otherwise
    """
    current_path = Path(__file__).resolve().parent

    for _ in range(max_depth):
        env_path = current_path / env_filename
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            print(f"[.env loaded from] {env_path}")
            return True
        current_path = current_path.parent

    print("[.env file not found]")
    return False

load_env_from_project_root()

@CrewBase
class GeneratePlanCrew():
    """GeneratePlanCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @property
    def llm_gemini(self):
        if not hasattr(self, "_llm_gemini"):
            api_key_gemini = os.environ["GEMINI_API_KEY"]
            if not api_key_gemini:
                raise ValueError("Missing GEMINI_API_KEY from environment")
            import google.generativeai as genai
            genai.configure(api_key=api_key_gemini)

            self._llm_gemini = LLM(
                model="gemini/gemini-2.5-pro-preview-05-06",
                temperature=0.1,
                reasoning_effort="high"
            )
        return self._llm_gemini
    
    @property
    def llm_groq(self):
        if not hasattr(self, "_llm_groq"):
            api_key_groq = os.environ["GROQ_API_KEY"]
            if not api_key_groq:
                raise ValueError("Missing GROQ_API_KEY from environment")
            self._llm_groq = LLM(
                model="groq/llama-3.3-70b-versatile",
                temperature=0.1,
                reasoning_effort="medium"
            )
        return self._llm_groq

    @before_kickoff
    def before_kickoff_function(self, inputs):
        return inputs

    @agent
    def business_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['business_designer'],
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
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
            llm=self.llm_groq,
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

