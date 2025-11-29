# PromptNova Project Overview

## 🚀 Introduction
PromptNova is an open-source AI prompt library and refinement tool. It allows users to discover, create, share, and refine AI prompts using advanced frameworks and multiple AI models.

## 🏗️ Architecture
The project follows a hybrid architecture:
- **Frontend**: A Next.js application (App Router) located in the `promptnova/` directory.
- **Backend**: A Python FastAPI application located in the root (`app.py`), which serves the API and the static frontend build.
- **AI Logic**: Powered by LangChain and LangGraph, located in `src/`.

## 🛠️ Tech Stack

### Frontend (`promptnova/`)
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4, Tailwind Merge, CLSX
- **UI Components**: Radix UI (Primitives), Lucide React (Icons)
- **Animations**: Framer Motion
- **Markdown**: React Markdown, Remark GFM, React Syntax Highlighter
- **State/Logic**: React 19

### Backend (Root)
- **Framework**: FastAPI
- **Language**: Python
- **AI Orchestration**: LangChain, LangGraph
- **AI Models**: 
  - Google Gemini (`langchain-google-genai`)
  - Groq (`langchain-groq`)
  - Mistral (`langchain-mistralai`)
- **Security**: `pycryptodome` (AES encryption for API keys)
- **Validation**: Pydantic

## 📂 Directory Structure

```
PromptNova/
├── app.py                      # Main FastAPI application entry point
├── requirements.txt            # Python dependencies
├── PROJECT_OVERVIEW.md         # Project documentation
├── src/                        # Backend Source Code
│   ├── agents/                 # AI Agent Implementations
│   │   ├── frameworks/         # Framework-specific agents (25 files: ape.py, co_star.py, etc.)
│   │   ├── types/              # Prompt type agents (33 files: chain_of_thought.py, etc.)
│   │   ├── evaluate/           # Evaluation agents
│   │   ├── project/            # Project generation agents
│   │   ├── refine/             # Refinement agents
│   │   ├── standard/           # Standard agents
│   │   ├── pick_agent.py       # Agent to select the best framework/type
│   │   └── prompt_agent.py     # Base prompt agent
│   ├── chains/                 # LangChain Pipelines
│   │   ├── pipeline.py         # Base pipeline logic
│   │   ├── evaluate_pipeline.py
│   │   ├── project_pipeline.py
│   │   ├── update_pipeline.py
│   │   └── project_update_pipeline.py
│   ├── models/                 # Pydantic Data Models
│   │   ├── prompt_schema.py
│   │   ├── evaluateSchema.py
│   │   ├── frameworkSchema.py
│   │   └── typesSchema.py
│   ├── config.py               # Configuration (API keys, etc.)
│   └── logger.py               # Logging setup
└── promptnova/                 # Frontend (Next.js) Source Code
    ├── package.json            # Frontend dependencies
    ├── next.config.ts          # Next.js configuration
    ├── tailwind.config.ts      # Tailwind CSS configuration
    ├── public/                 # Static assets (images, icons)
    └── src/
        ├── app/                # Next.js App Router
        │   ├── page.tsx        # Home page
        │   ├── layout.tsx      # Root layout
        │   ├── globals.css     # Global styles
        │   ├── about/          # About page
        │   ├── evaluate/       # Evaluation page
        │   └── guide/          # Guide pages
        ├── components/         # React Components
        │   ├── Home/           # Home page specific components
        │   │   ├── Form.tsx
        │   │   ├── RefineForm.tsx
        │   │   ├── ResultDisplay.tsx
        │   │   └── ...
        │   ├── ui/             # Reusable UI components (Radix UI wrappers)
        │   │   ├── button.tsx
        │   │   ├── card.tsx
        │   │   ├── input.tsx
        │   │   └── ...
        │   ├── Navbar.tsx
        │   ├── Footer.tsx
        │   └── ThemeProvider.tsx
        └── lib/                # Utility functions
```

### Key Files Description
- **`app.py`**: The heart of the backend. It sets up the FastAPI server, handles CORS, decrypts API keys, and routes requests to the appropriate LangChain pipelines. It also serves the compiled Next.js frontend.
- **`src/chains/pipeline.py`**: Orchestrates the flow of data through the AI models.
- **`promptnova/src/components/Home/Form.tsx`**: The main user interface for inputting prompts and selecting options.


## 🔑 Key Features
1.  **Prompt Refinement**: Users can refine prompts using specific styles and frameworks.
2.  **Project Generation**: Generates comprehensive prompts for entire projects.
3.  **Evaluation**: A multi-agent pipeline to evaluate prompt quality.
4.  **Model Selection**: Users can choose between Gemini, Groq, and Mistral models.
5.  **Secure API Keys**: API keys are encrypted before being sent to the backend.

## 🏃‍♂️ How to Run
1.  **Backend**:
    ```bash
    pip install -r requirements.txt
    uvicorn app:app --reload
    ```
2.  **Frontend**:
    ```bash
    cd promptnova
    npm install
    npm run dev
    ```
