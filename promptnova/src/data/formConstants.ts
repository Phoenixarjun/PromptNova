export interface Example {
  id: number;
  input: string;
  output: string;
}

export interface AdvancedParams {
  types?: { [key: string]: { [key: string]: string } };
  framework?: { [key: string]: { [key: string]: string } };
}

export interface ValidationError {
  loc?: (string | number)[];
  msg?: string;
}

export interface ProjectParams {
  objective?: string;
  scope?: string;
  domain?: string;
  constraints?: string;
  resources?: string;
  timeline?: string;
  stakeholders?: string;
  deliverables?: string;
  risks?: string;
  dependencies?: string;
  success_criteria?: string;
  budget?: string;
  technology_stack?: string;
  milestones?: string;
  requirements?: string;
  context?: string;
}



export const combos = [
  {
    name: "Custom",
    description: "Select your own combination of types and framework.",
    types: [] as string[],
    framework: null as string | null,
  },
  {
    name: "Universal Adaptive Engine",
    description: "Goal: adaptable to any task type — coding, writing, analysis, or planning. This combo integrates Chain-of-Thought for reasoning, Role prompting for contextual expertise, Retrieval-Augmented Prompting for factual grounding, and Reflexion for self-correction, unified under the Co-Star framework for balanced performance and reliability.",
    types: ['cot', 'role', 'retrieval_augmented_prompting', 'reflexion_type'],
    framework: 'co_star',
  },
  {
    name: "Build Clean Code with Expert Guidance",
    description: "Goal: robust, well-structured code with explanations. This combo uses Step-by-Step Reasoning, Role-Based Expertise, and advanced decomposition techniques within the Co-Star framework to produce high-quality code.",
    types: ['cot', 'role', 'task_decomposition', 'tot'],
    framework: 'co_star',
  },
  {
    name: "Create Compelling Content",
    description: "Goal: engaging blog posts, articles, or marketing copy. This combo uses directional nudges, emotional infusion, and knowledge generation with examples under the CRISPE framework to create persuasive content.",
    types: ['directional_stimulus', 'emotion', 'generated_knowledge', 'few_shot'],
    framework: 'crispe',
  },
  {
    name: "Smart Problem Solver",
    description: "Goal: solve a tricky problem or plan something. This combo uses progressive reasoning, self-correction, and task decomposition with Automatic Prompt Engineering to break down and solve complex problems.",
    types: ['least_to_most', 'task_decomposition', 'automatic_prompt_engineering'],
    framework: 'ape',
  },
  {
    name: "Creative Idea Generator",
    description: "Goal: creative ideas for projects, features, names, etc. This combo uses multi-tasking, emotional appeal, and knowledge injection within the Co-Star framework to spark innovative ideas.",
    types: ['multi_task', 'emotion', 'generated_knowledge'],
    framework: 'co_star',
  },
  {
    name: "Advanced Reasoning + Verification",
    description: "Goal: High-accuracy logic-heavy outputs like coding, math, or decision-making. This combo uses Chain-of-Thought for step-by-step reasoning, Chain-of-Verification for correctness, and Task Decomposition to split complex tasks, all orchestrated by the Co-Star framework.",
    types: ['cot', 'chain_of_verification', 'task_decomposition'],
    framework: 'co_star',
  },
  {
    name: "Creative Content + Roleplay",
    description: "Goal: Writing, marketing content, or brainstorming ideas. This combo uses Role Assignment for creativity, Few-Shot examples for consistency, and ReAct to take external actions, all within the Tool-Oriented Prompting framework to connect with creative tools.",
    types: ['role', 'few_shot', 'react'],
    framework: 'tool_oriented_prompting',
  },
  {
    name: "Research + Analysis",
    description: "Goal: Knowledge-heavy tasks like report generation or research synthesis. This combo uses Retrieval-Augmented Prompting to fetch data, Active-Prompt to self-correct, and Reflexion to iteratively improve, all structured by the Neuro-Symbolic framework for explainable reasoning.",
    types: ['retrieval_augmented_prompting', 'active_prompt', 'reflexion_type', 'skeleton_of_thought'],
    framework: 'neuro_symbolic_prompting',
  },
  {
    name: "Long-Term Planning + Multi-Context Tasks",
    description: "Goal: Strategic planning, project management, or multi-step execution. This combo uses Plan-and-Solve to separate planning from execution, Context Expansion to maintain relevant info, and Multi-Agent Debate for diverse evaluation, all managed by Dynamic Context Windows for long-session continuity.",
    types: ['plan_and_solve', 'context_expansion', 'multi_agent_debate', 'goal_oriented_prompting'],
    framework: 'dynamic_context_windows',
  },
  {
  name: "Analytical Thinker + Self-Aware Optimizer",
  description: "Goal: analytical reasoning and optimization. This combo employs Skeleton-of-Thought for structured reasoning, Reflexion for iterative self-assessment, and Meta-Cognitive Prompting for adaptive refinement, orchestrated through the PRISM framework for clarity and precision.",
  types: ['skeleton_of_thought', 'reflexion', 'meta_cognitive_prompting', 'chain_of_verification'],
  framework: 'prism',
},
{
  name: "Innovative Story Architect",
  description: "Goal: build imaginative stories or experiential content. This combo blends Emotion for human depth, Persona Switching for dynamic character voices, Scaffolded Prompting for structured creativity, and Multi-Task for parallel narrative elements, using the SCOPE framework for contextual coherence.",
  types: ['emotion', 'persona_switching', 'scaffolded_prompting', 'multi_task'],
  framework: 'scope',
},
{
  name: "Universal Adaptive Engine",
  description: "Goal: adaptable to any task type — coding, writing, analysis, or planning. This combo integrates Chain-of-Thought for reasoning, Role prompting for contextual expertise, Retrieval-Augmented Prompting for factual grounding, and Reflexion for self-correction, unified under the Co-Star framework for balanced performance and reliability.",
  types: ['cot', 'role', 'retrieval_augmented_prompting', 'reflexion'],
  framework: 'co_star',
}

];

export const types = [
  { name: 'Zero Shot', slug: 'zero_shot' },
  { name: 'One Shot', slug: 'one_shot' },
  { name: 'Chain of Thought (CoT)', slug: 'cot' },
  { name: 'Tree of Thought (ToT)', slug: 'tot' },
  { name: 'ReAct', slug: 'react' },
  { name: 'In Context', slug: 'in_context' },

  { name: 'Role', slug: 'role' },
  { name: 'Few Shot', slug: 'few_shot' },
  { name: 'Self Consistency', slug: 'self_consistency' },
  { name: 'Meta Prompting', slug: 'meta_prompting' },
  { name: 'Least to Most', slug: 'least_to_most' },
  { name: 'Multi Task', slug: 'multi_task' },
  { name: 'Task Decomposition', slug: 'task_decomposition' },
  { name: 'Constrained', slug: 'constrained' },
  { name: 'Generated Knowledge', slug: 'generated_knowledge' },
  { name: 'Automatic Prompt Engineering', slug: 'automatic_prompt_engineering' },
  { name: 'Directional Stimulus', slug: 'directional_stimulus' },
  { name: 'Chain-of-Verification (CoVe)', slug: 'chain_of_verification' },
  { name: 'Skeleton-of-Thought (SoT)', slug: 'skeleton_of_thought' },
  { name: 'Graph-of-Thoughts (GoT)', slug: 'graph_of_thoughts' },
  { name: 'Plan-and-Solve (PS)', slug: 'plan_and_solve' },
  { name: 'Maieutic Prompting', slug: 'maieutic_prompting' },
  { name: 'Reflexion', slug: 'reflexion_type' },
  { name: 'Chain-of-Density (CoD)', slug: 'chain_of_density' },
  { name: 'Active-Prompt', slug: 'active_prompt' },
  { name: 'Retrieval-Augmented (RAP)', slug: 'retrieval_augmented_prompting' },
  { name: 'Multi-Agent Debate', slug: 'multi_agent_debate' },
  { name: 'Emotion', slug: 'emotion' },
  { name: 'Persona Switching', slug: 'persona_switching' },
  { name: 'Scaffolded Prompting', slug: 'scaffolded_prompting' },
  { name: 'Deliberation Prompting', slug: 'deliberation_prompting' },
  { name: 'Context Expansion', slug: 'context_expansion' },
  { name: 'Goal-Oriented Prompting', slug: 'goal_oriented_prompting' },
];

export const frameworks = [
  { name: 'Co-Star', slug: 'co_star' },
  { name: 'TCEF', slug: 'tcef' },
  { name: 'CRISPE', slug: 'crispe' },
  { name: 'ICE', slug: 'ice' },
  { name: 'CRAFT', slug: 'craft' },
  { name: 'APE', slug: 'ape' },
  { name: 'PECRA', slug: 'pecra' },
  { name: 'OSCAR', slug: 'oscar' },
  { name: 'RASCE', slug: 'rasce' },
  { name: 'Reflection', slug: 'reflection' },
  { name: 'Flipped Interaction', slug: 'flipped_interaction' },
  { name: 'BAB', slug: 'bab' },
  { name: 'PROMPT Framework', slug: 'prompt' },
  { name: 'CLEAR', slug: 'clear' },
  { name: 'PRISM', slug: 'prism' },
  { name: 'GRIPS', slug: 'grips' },
  { name: 'APP', slug: 'app' },
  { name: 'SOAP', slug: 'soap' },
  { name: 'SCOPE', slug: 'scope' },
  { name: 'Tool-Oriented Prompting (TOP)', slug: 'tool_oriented_prompting' },
  { name: 'Neuro-Symbolic Prompting', slug: 'neuro_symbolic_prompting' },
  { name: 'Dynamic Context Windows', slug: 'dynamic_context_windows' },
  { name: 'Meta-Cognitive Prompting', slug: 'meta_cognitive_prompting' },
  { name: 'Prompt Ensembles', slug: 'prompt_ensembles' },
];

export const projectParamsSchema: { [key in keyof Omit<ProjectParams, 'framework'>]: { label: string, description: string } } = {
  objective: { label: "Objective", description: "The goal of the project." },
  scope: { label: "Scope", description: "Key features and functionalities." },
  domain: { label: "Domain", description: "The specific industry for the project." },
  constraints: { label: "Constraints", description: "Any limitations to consider." },
  resources: { label: "Resources", description: "Available resources (e.g., budget, team size)." },
  timeline: { label: "Timeline", description: "The project timeline or deadline." },
  stakeholders: { label: "Stakeholders", description: "Key people involved in the project." },
  deliverables: { label: "Deliverables", description: "Expected outputs from the project." },
  risks: { label: "Risks", description: "Potential challenges or risks." },
  dependencies: { label: "Dependencies", description: "Project dependencies on other systems." },
  success_criteria: { label: "Success Criteria", description: "How project success will be measured." },
  budget: { label: "Budget", description: "The allocated budget for the project." },
  technology_stack: { label: "Technology Stack", description: "The technology stack to be used." },
  milestones: { label: "Milestones", description: "Key phases or milestones in the project." },
  requirements: { label: "Requirements", description: "Specific requirements or specifications." },
  context: { label: "Context", description: "Optional background context for the task." },
};
