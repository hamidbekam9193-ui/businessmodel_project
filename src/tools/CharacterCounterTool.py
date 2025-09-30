from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class CharacterCounterInput(BaseModel):
    """Input schema for the CharacterCounterTool."""
    text_to_count: str = Field(..., description="The block of text for which the characters need to be counted.")

class CharacterCounterTool(BaseTool):
    name: str = "Character Counter"
    description: str = "Counts the number of characters in a given text. Useful for ensuring the output adheres to length constraints."
    args_schema: Type[BaseModel] = CharacterCounterInput

    def _run(self, text_to_count: str) -> str:
        """
        Counts the characters in the provided text.

        Args:
            text_to_count (str): The text whose characters will be counted.

        Returns:
            str: A confirmation message indicating the character count.
        """
        count = len(text_to_count)
        return f"Character count is: {count}"
