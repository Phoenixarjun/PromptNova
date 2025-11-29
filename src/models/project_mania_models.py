from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

class ProjectManiaSchema(BaseModel):
    """Input schema for Project Mania generation."""
    intent: str = Field(..., description="The user's intent for the template.")
    variables: List[str] = Field(..., description="List of variables to include in the template.")
    template_type: Literal["general", "crewai", "autogen"] = Field(..., description="The type of template to generate.")
    prompt_length: Literal["low", "medium", "high"] = Field("medium", description="Desired length/verbosity of the generated template.")
    api_key: Optional[str] = Field(None, description="User's API key.")
    password: Optional[str] = Field(None, description="Password to decrypt the API key.")
    selected_model: Optional[str] = Field("gemini", description="Selected LLM provider.")
    selected_groq_model: Optional[str] = Field(None, description="Selected Groq model.")

class ProjectManiaResponse(BaseModel):
    """Output schema for Project Mania generation."""
    final_template: str = Field(..., description="The final refined template.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata about the generation process.")
