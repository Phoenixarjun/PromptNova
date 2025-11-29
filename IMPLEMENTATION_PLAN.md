# Implementation Plan - Project Mania

## Goal Description
Add a new feature called **Project Mania** to PromptNova. This feature allows users to generate blueprint templates for General Prompts, CrewAI, and AutoGen based on intent and variables. It involves a new backend workflow with a router, composers, and a refinement pipeline, and a new frontend page with a dedicated form.

## User Review Required
> [!IMPORTANT]
> This plan involves adding a new API endpoint and a new frontend route. Please ensure no conflicts with existing routes.

## Proposed Changes

### Backend

#### Models
- [NEW] `src/models/project_mania_models.py`: Define `ProjectManiaSchema` and related models.

#### Agents
- [NEW] `src/agents/project_mania/__init__.py`
- [NEW] `src/agents/project_mania/router_agent.py`: Selects the composer.
- [NEW] `src/agents/project_mania/composers/generic_template_composer.py`: General prompt composer.
- [NEW] `src/agents/project_mania/composers/crewai_template_composer.py`: CrewAI composer.
- [NEW] `src/agents/project_mania/composers/autogen_template_composer.py`: AutoGen composer.
- [NEW] `src/agents/project_mania/refine/analyze_agent.py`: Analyzes draft templates.
- [NEW] `src/agents/project_mania/refine/refine_agent.py`: Refines templates based on analysis.
- [NEW] `src/agents/project_mania/refine/evaluate_agent.py`: Evaluates if the template is ready.

#### Chains
- [NEW] `src/chains/project_mania_refinement_pipeline.py`: Implements the Analyze -> Refine -> Evaluate loop.
- [NEW] `src/chains/project_mania_pipeline.py`: Orchestrates the full flow.

#### API
- [MODIFY] `app.py`: Add `POST /api/project-mania/generate` endpoint.

### Frontend

#### API
- [NEW] `promptnova/src/lib/projectManiaApi.ts`: API client for the new endpoint.

#### Components
- [NEW] `promptnova/src/components/ProjectMania/Form.tsx`: Dedicated form for Project Mania.
- [NEW] `promptnova/src/components/ProjectMania/ResultDisplay.tsx`: Result display for Project Mania (or reuse if identical). *Decision: Create wrapper or copy to ensure isolation as requested.*

#### Pages
- [NEW] `promptnova/src/app/project-mania/page.tsx`: Main page for Project Mania.

#### Navigation
- [MODIFY] `promptnova/src/components/Navbar.tsx`: Add link to Project Mania.

## Verification Plan

### Automated Tests
- None specified in the prompt, but I will verify by running the server and checking the endpoint.

### Manual Verification
1.  Start backend (`uvicorn app:app --reload`).
2.  Start frontend (`npm run dev`).
3.  Navigate to `/project-mania`.
4.  Enter intent, variables, and select template type.
5.  Submit and verify the generated template.
