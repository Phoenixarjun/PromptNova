from pydantic import BaseModel, Field
from typing import Optional, Literal


class ProjectManagerInput(BaseModel):
    """Input schema for Project Manager."""
    framework: Literal["project_manager"] = "project_manager"
    api_key: Optional[str] = Field(None, description="API key for the selected model provider.")
    password: Optional[str] = Field(None, description="Password for decrypting the API key.")
    selected_model: Optional[str] = Field("gemini", description="The model provider to use (e.g., 'gemini', 'groq', 'mistral').")
    selected_groq_model: Optional[str] = Field("llama3-8b-8192", description="The specific Groq model to use.")
    
    user_input: str = Field(..., description="The user's core idea or problem statement for the project.")
    objective: Optional[str] = Field(None, description="The goal of the project.")
    scope: Optional[str] = Field(None, description="The scope of the project, including key features and functionalities.")
    domain: Optional[str] = Field(None, description="The specific domain or industry the project is related to.")
    constraints: Optional[str] = Field(None, description="Any constraints or limitations that need to be considered.")
    resources: Optional[str] = Field(None, description="Resources available for the project (e.g., budget, team size, technology stack).")
    timeline: Optional[str] = Field(None, description="The timeline or deadline for the project.")
    stakeholders: Optional[str] = Field(None, description="Key stakeholders involved in the project.")
    deliverables: Optional[str] = Field(None, description="Expected deliverables from the project.")
    risks: Optional[str] = Field(None, description="Potential risks or challenges that might be encountered.")
    dependencies: Optional[str] = Field(None, description="Any dependencies the project has on other projects or systems.")
    success_criteria: Optional[str] = Field(None, description="Criteria for determining the success of the project.")
    budget: Optional[str] = Field(None, description="The budget allocated for the project.")
    technology_stack: Optional[str] = Field(None, description="The technology stack to be used.")
    milestones: Optional[str] = Field(None, description="Key milestones or phases in the project.")
    requirements: Optional[str] = Field(None, description="Specific requirements or specifications for the project.")
    team: Optional[str] = Field(None, description="The team members involved and their roles.")
    context: Optional[str] = Field(None, description="Optional background context for the task.")