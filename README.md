# 🚀 PromptNova – Your Open-Source AI Prompt Engineering Workbench

<img width="1898" height="866" alt="PromptNova Banner" src="https://github.com/user-attachments/assets/728ec65d-6968-4368-8819-579356c2e6f9" />

> **Discover, Refine, and Optimize.**  
> PromptNova is an open-source platform to craft, compile, and evaluate high-performance AI prompts, built for developers, researchers, and creators to unlock the full reasoning potential of modern language models.

---

## 💡 The Problem: Performance Under-Supply (PUX)

In the rapidly evolving world of generative AI, crafting the perfect prompt is an engineering discipline. While Large Language Models (LLMs) are exceptionally capable, most users rely on basic zero-shot instructions, unaware of the vast array of structured prompt engineering **types and frameworks** that exist.

This leads to **"Performance Under-Supply" (PUX)**—a state where models operate at only a fraction of their true reasoning potential. PromptNova solves this by serving as an intelligent compilation and evaluation engine that structures raw user intent into production-grade prompts and multi-agent templates.

---

## 🚀 Tech Stack

### 🔖 Tags

![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-0052CC?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-0052CC?style=for-the-badge)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F4370A?style=for-the-badge)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-FF7000?style=for-the-badge)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

---

### 🧠 Why These Technologies?

| Technology | Purpose |
|---|---|
| **Next.js 16** | Modern React framework providing a fast, responsive user interface with static optimization and export. |
| **React 19** | Powers the dynamic, component-based frontend and reactive form states. |
| **TypeScript** | Ensures end-to-end type safety and developer ergonomics across frontend components and schemas. |
| **Tailwind CSS 4** | Rapid utility-first styling with native OKLCH tokens and dark mode support. |
| **FastAPI** | High-performance asynchronous Python web framework orchestrating the AI agent backend. |
| **LangGraph** | Builds stateful, multi-actor cyclical workflows for iterative prompt self-correction and evaluation. |
| **LangChain** | Provides prompt templates, output parsers, and multi-provider model abstractions. |
| **Gemini AI** | Primary frontier engine (Gemini 2.5 Flash) for high-accuracy prompt synthesis and critique. |
| **Groq** | LPU inference engine executing high-speed open-weights models (DeepSeek-R1-Distill, LLaMA 3.3). |
| **Mistral AI** | Alternative frontier model provider (Mistral Large) for complex reasoning tasks. |
| **Web Speech API** | Browser-native voice input for hands-free prompt dictation without external dependencies. |
| **Git** | Distributed version control for collaborative development and release tracking. |

---

## 🌟 Key Features

### 🔍 Intelligent Agent Picker (`/pick_agent`)
Not sure which prompting technique fits your task? The autonomous agent picker analyzes your raw text and automatically selects the most effective 3–5 prompt types and 1 complementary framework.

### ✍️ Multi-Style Prompt Compilation (`/refine`)
Transform simple instructions into expert-level prompts by combining up to 5 prompting styles (Zero-Shot, Few-Shot, CoT, ToT, ReAct, Self-Consistency, Reflexion, etc.) and a structured framework (CO-STAR, CRISPE, TCEF, RTF, etc.) inside a stateful LangGraph refinement loop.

### 📊 Multi-Perspective Prompt Evaluation (`/evaluate`)
Objectively evaluate prompt quality across multiple independent evaluation frameworks in parallel via `asyncio.gather`:
- **LLM-as-a-Judge**: Evaluates clarity, specificity, context completeness, goal alignment, and measurability.
- **T-RAG**: Measures intent alignment, instruction completeness, relevance, and ambiguity.
- **MAR Framework**: Scores clarity, completeness, structure, and creativity-precision balance to generate an overall normalized quality score (0–100).

### 🤖 Project Mania – Multi-Agent Blueprints (`/project-mania`)
Generate turnkey, framework-ready code templates and configurations for:
- **CrewAI**: Full agent and task definitions with role-based personas.
- **AutoGen**: Conversable multi-agent system configurations.
- **Generic Jinja**: Flexible parameterized prompt templates.

### 📖 Interactive Prompt Engineering Guide (`/guide`)
Explore an offline, statically pre-rendered encyclopedia explaining 33 prompt engineering types and 24 frameworks with concrete examples, pros, and cons.

### 🔄 Conversational Refinement Loops
Iteratively refine generated prompts or project blueprints with natural language critique through human-in-the-loop update pipelines.

---

## 🖼️ Screenshots

<img width="1890" height="864" alt="PromptNova App Interface" src="https://github.com/user-attachments/assets/957e6a84-36aa-4341-9433-50001bddfc04" />

<img width="1886" height="862" alt="Prompt Evaluation Interface" src="https://github.com/user-attachments/assets/d5e620db-afa0-48bb-bf47-7dc691109c33" />

<img width="1886" height="862" alt="Project Mania Interface" src="https://github.com/user-attachments/assets/1e836915-41d3-4939-be89-b530b993f485" />

---

## 🔗 Live Demo

**🌍 [Visit PromptNova Now →](https://prompt-nova.vercel.app/)**  
Fully responsive. Works seamlessly across desktop and mobile devices.

---

## 🧪 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Phoenixarjun/PromptNova.git
cd PromptNova
```

### 2. Set up and start the Backend (FastAPI)
```bash
# Create and activate a Python virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables in a .env file:
# GOOGLE_API_KEY=your_gemini_api_key
# GROQ_API_KEY=your_groq_api_key (optional)
# MISTRAL_API_KEY=your_mistral_api_key (optional)

# Run the FastAPI server
uvicorn app:app --reload --port 8000
```

### 3. Set up and start the Frontend (Next.js)
In a separate terminal:
```bash
cd promptnova

# Install dependencies
npm install

# Start the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧑‍💻 Author

**Naresh B A** – Full Stack Developer & AI/ML Enthusiast

- **GitHub**: [@Phoenixarjun](https://github.com/Phoenixarjun)
- **Portfolio**: [naresh-portfolio-007.netlify.app](https://naresh-portfolio-007.netlify.app/)

---

## ⚡ License & Contributions

PromptNova is open-source software licensed under the [MIT License](LICENSE). Pull requests and contributions are welcome!
