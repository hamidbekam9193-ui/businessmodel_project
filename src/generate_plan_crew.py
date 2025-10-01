# --- START OF FILE src/generate_plan_crew.py ---

import os
from typing import Optional

import yaml

# external LLM libraries (optional imports handled during runtime)
try:
    from google import genai
    from google.genai import types # Import types for configuration
except Exception:
    genai = None
    types = None # Set types to None if genai is not available

try:
    from langchain_groq import ChatGroq
except Exception:
    ChatGroq = None

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff

# NOTE: CharacterCounterTool must be defined/imported from your project.
# If you have a concrete implementation, replace the placeholder below with:
# from your_tools import CharacterCounterTool
class CharacterCounterTool:
    """Placeholder CharacterCounterTool. Replace with your real implementation."""
    def __init__(self):
        pass


@CrewBase
class GeneratePlanCrew:
    """GeneratePlanCrew crew"""

    # Paths to YAML config files for agents and tasks
    agents_config_path = "config/agents.yaml"
    tasks_config_path = "config/tasks.yaml"

    def __init__(self, gemini_api_key: Optional[str] = None, groq_api_key: Optional[str] = None):
        """
        Constructor accepts API keys dynamically.
        Keys are expected to be passed from the application entrypoint.
        """
        self._gemini_api_key = gemini_api_key
        self._groq_api_key = groq_api_key

        # lazy-loaded LLM instances
        self._llm_gemini = None
        self._llm_groq = None

        # load agent/task configs (if present)
        self.agents_config = self._load_yaml(self.agents_config_path) or {}
        self.tasks_config = self._load_yaml(self.tasks_config_path) or {}

    def _load_yaml(self, path: str):
        """Load a YAML file and return its contents as a dict, or None if not found."""
        if not path:
            return None
        try:
            base = os.getcwd()
            full_path = path if os.path.isabs(path) else os.path.join(base, path)
            if not os.path.exists(full_path):
                return None
            with open(full_path, "r", encoding="utf-8") as fh:
                return yaml.safe_load(fh)
        except Exception:
            # don't crash on config load — return None and let callers handle missing keys
            return None

    @property
    def llm_gemini(self):
        """Lazy-init a Gemini LLM wrapper (LLM from crewai configured to use Gemini)."""
        if self._llm_gemini is None:
            if not self._gemini_api_key:
                raise ValueError("Gemini API key not provided to GeneratePlanCrew.")
            if genai is None or types is None:
                raise ImportError("google.generativeai is not installed or could not be imported.")

            # Create a single client object for the new SDK
            genai_client = genai.Client(api_key=self._gemini_api_key)

            # create crewai LLM object for Gemini (model string based on user's choice)
            self._llm_gemini = LLM(
                model="gemini/gemini-2.5-pro-preview-05-06", # This model string might need adjustment based on crewai's expected format for the new SDK
                temperature=0.1,
                reasoning_effort="high",
                client=genai_client # Pass the initialized client to the LLM
            )
        return self._llm_gemini

    @property
    def llm_groq(self):
        """Lazy-init a Groq-backed LLM via ChatGroq (langchain_groq)."""
        if self._llm_groq is None:
            if not self._groq_api_key:
                raise ValueError("Groq API key not provided to GeneratePlanCrew.")
            if ChatGroq is None:
                raise ImportError("langchain_groq.ChatGroq is not available/imported.")
            # instantiate the ChatGroq object -- the exact args depend on the version of langchain_groq
            self._llm_groq = ChatGroq(
                temperature=0.1,
                groq_api_key=self._groq_api_key,
                model_name="llama-3.3-70b-versatile"
            )
        return self._llm_groq

    @before_kickoff
    def before_kickoff_function(self, inputs):
        """
        Inputs provided by the user (form data).
        API keys are NOT expected here because they're passed to __init__.
        """
        return inputs

    # ---------- Agents ----------
    # Each agent pulls config by name from the loaded agents_config dict.
    # If the config file isn't present or doesn't contain the specific agent entry,
    # we fall back to passing the name string to Agent (depending on how crewai expects it).
    def _agent_config_or_name(self, name: str):
        return self.agents_config.get(name) if isinstance(self.agents_config, dict) else name

    @agent
    def business_designer(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("business_designer"),
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def product_designer(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("product_designer"),
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def market_analyst(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("market_analyst"),
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def marketing_expert(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("marketing_expert"),
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def operations_specialist(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("operations_specialist"),
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def financial_expert(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("financial_expert"),
            tools=[CharacterCounterTool()],
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def consolidator(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("consolidator"),
            llm=self.llm_gemini,
            verbose=True
        )

    @agent
    def evaluator(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("evaluator"),
            llm=self.llm_groq,
            verbose=True
        )

    @agent
    def refiner(self) -> Agent:
        return Agent(
            config=self._agent_config_or_name("refiner"),
            llm=self.llm_groq,
            verbose=True
        )

    # ---------- Tasks ----------
    def _task_config_or_name(self, name: str):
        return self.tasks_config.get(name) if isinstance(self.tasks_config, dict) else name

    @task
    def create_business_concept(self) -> Task:
        return Task(config=self._task_config_or_name("create_business_concept"))

    @task
    def create_product_design(self) -> Task:
        return Task(config=self._task_config_or_name("create_product_design"),
                    context=[self.create_business_concept()])

    @task
    def create_market_analysis(self) -> Task:
        return Task(config=self._task_config_or_name("create_market_analysis"),
                    context=[self.create_business_concept(), self.create_product_design()])

    @task
    def create_marketing_plan(self) -> Task:
        return Task(config=self._task_config_or_name("create_marketing_plan"),
                    context=[self.create_business_concept(), self.create_product_design(), self.create_market_analysis()])

    @task
    def create_operating_plan(self) -> Task:
        return Task(config=self._task_config_or_name("create_operating_plan"),
                    context=[self.create_business_concept(), self.create_product_design(), self.create_market_analysis(), self.create_marketing_plan()])

    @task
    def create_financial_plan(self) -> Task:
        return Task(config=self._task_config_or_name("create_financial_plan"),
                    context=[self.create_business_concept(), self.create_product_design(), self.create_market_analysis(), self.create_marketing_plan(), self.create_operating_plan()])

    @task
    def consolidate_plan(self) -> Task:
        return Task(config=self._task_config_or_name("consolidate_plan"),
                    context=[self.create_business_concept(), self.create_product_design(), self.create_market_analysis(), self.create_marketing_plan(), self.create_operating_plan(), self.create_financial_plan()])

    @task
    def evaluate_plan(self) -> Task:
        return Task(config=self._task_config_or_name("evaluate_plan"),
                    context=[self.consolidate_plan()])

    @task
    def refine_plan(self) -> Task:
        return Task(config=self._task_config_or_name("refine_plan"),
                    context=[self.consolidate_plan(), self.evaluate_plan()])

    # ---------- Crew ----------
    @crew
    def crew(self) -> Crew:
        """Creates the GeneratePlanCrew crew"""
        # Ensure LLMs are initialized by accessing their properties so any import errors are raised early
        _ = self.llm_gemini
        _ = self.llm_groq

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def run(self, inputs: dict = None):
        """
        Kick off the crew with provided inputs.
        Any exceptions are wrapped to add context.
        """
        try:
            return self.crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"Error while running the crew: {e}") from e

# --- END OF FILE src/generate_plan_crew.py ---
