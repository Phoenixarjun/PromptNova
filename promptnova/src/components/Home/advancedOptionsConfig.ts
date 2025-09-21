export interface Field {
  name: string;
  label: string;
  type: 'text' | 'textarea' | 'number';
  description: string;
}

export const advancedTypeOptions: { [key: string]: Field[] } = {
    one_shot: [
      { name: 'example_input', label: 'Example Input', type: 'textarea', description: 'An example of the input you would provide.' },
      { name: 'example_output', label: 'Example Output', type: 'textarea', description: 'The corresponding output you expect.' },
    ],
    cot: [
      { name: 'steps', label: 'Reasoning Steps', type: 'number', description: 'Optional number of reasoning steps to enforce.' },
    ],
    tot: [
      { name: 'branches', label: 'Reasoning Branches', type: 'number', description: 'Number of reasoning branches to explore (default: 3).' },
    ],
    react: [
      { name: 'max_iterations', label: 'Max Iterations', type: 'number', description: 'Maximum reasoning-action iterations (default: 3).' },
    ],
    in_context: [
      { name: 'context', label: 'Context', type: 'textarea', description: 'Context to include in the prompt.' },
    ],
    emotion: [
      { name: 'emotion', label: 'Emotion', type: 'text', description: 'Emotion to infuse in the prompt (e.g., excited, empathetic).' },
    ],
    role: [
      { name: 'role_persona', label: 'Role Persona', type: 'text', description: 'The professional role for the AI (e.g., expert, senior developer).' },
    ],
    few_shot: [],
    self_consistency: [
      { name: 'samples', label: 'Consistency Samples', type: 'number', description: 'Number of samples for consistency voting (default: 3).' },
    ],
    meta_prompting: [
      { name: 'iterations', label: 'Improvement Iterations', type: 'number', description: 'Number of iterations to improve the prompt (default: 2).' },
    ],
    least_to_most: [
      { name: 'sub_tasks', label: 'Sub-tasks (comma-separated)', type: 'text', description: 'List of sub-tasks to break down the prompt.' },
    ],
    multi_task: [
      { name: 'tasks', label: 'Related Tasks (comma-separated)', type: 'text', description: 'List of related tasks to include in the prompt.' },
    ],
    task_decomposition: [
      { name: 'sub_steps', label: 'Sub-steps (comma-separated)', type: 'text', description: 'List of sub-steps to decompose the task.' },
    ],
    constrained: [
      { name: 'max_words', label: 'Max Words', type: 'number', description: 'Maximum word count for the refined prompt.' },
      { name: 'output_format', label: 'Output Format', type: 'text', description: 'Desired output format (e.g., bullet points, JSON).' },
    ],
    generated_knowledge: [
      { name: 'facts_count', label: 'Facts to Generate', type: 'number', description: 'Number of facts to generate before refining (default: 3).' },
    ],
    automatic_prompt_engineering: [
      { name: 'optimization_goal', label: 'Optimization Goal', type: 'text', description: 'Goal for prompt optimization (e.g., clarity, brevity).' },
    ],
    directional_stimulus: [
      { name: 'focus', label: 'Focus Area', type: 'text', description: 'Specific focus area for the prompt (e.g., practical applications).' },
    ],
    chain_of_verification: [
        { name: 'verification_steps', label: 'Verification Steps', type: 'number', description: 'Number of verification steps to perform.' },
    ],
    skeleton_of_thought: [
        { name: 'focus_points', label: 'Focus Points', type: 'number', description: 'Number of focus points in the thought skeleton.' },
    ],
    plan_and_solve: [
        { name: 'plan_steps', label: 'Planning Steps', type: 'number', description: 'Number of planning steps before solution.' },
    ],
    maieutic_prompting: [
        { name: 'question_depth', label: 'Questioning Depth', type: 'number', description: 'Depth of guided questioning for eliciting answers.' },
    ],
    reflexion_type: [
        { name: 'reflection_criteria', label: 'Reflection Criteria', type: 'text', description: 'Criteria for self-reflection (e.g., clarity, accuracy).' },
    ],
    chain_of_density: [
        { name: 'density_level', label: 'Density Level', type: 'text', description: 'Density of reasoning steps (low, medium, high).' },
    ],
    retrieval_augmented_prompting: [
        { name: 'knowledge_sources', label: 'Knowledge Sources (comma-separated)', type: 'text', description: 'External sources/databases to retrieve knowledge from.' },
    ],
    multi_agent_debate: [
        { name: 'agents_count', label: 'Number of Agents', type: 'number', description: 'Number of agents participating in the debate.' },
    ],
    persona_switching: [
        { name: 'personas', label: 'Personas (comma-separated)', type: 'text', description: 'List of personas to switch between.' },
    ],
    scaffolded_prompting: [
        { name: 'scaffold_levels', label: 'Scaffold Levels', type: 'number', description: 'Number of scaffold levels for guidance.' },
    ],
    deliberation_prompting: [
        { name: 'passes', label: 'Deliberation Passes', type: 'number', description: 'Number of deliberation passes for refining output.' },
    ],
    context_expansion: [
        { name: 'max_expansion_tokens', label: 'Max Expansion Tokens', type: 'number', description: 'Maximum number of tokens to expand context.' },
    ],
    goal_oriented_prompting: [
        { name: 'goal', label: 'Goal', type: 'text', description: 'The goal the AI should focus on achieving.' },
        { name: 'success_criteria', label: 'Success Criteria', type: 'text', description: 'Criteria for evaluating success (e.g., accuracy, completeness).' },
    ],
  };
  
  export const advancedFrameworkOptions: { [key: string]: Field[] } = {
    co_star: [
      { name: 'context', label: 'Context', type: 'textarea', description: 'Optional background context for the task.' },
      { name: 'objective', label: 'Objective', type: 'textarea', description: 'Optional goal of the task.' },
      { name: 'style', label: 'Style', type: 'text', description: 'Optional style for the output (e.g., bullet points, narrative).' },
      { name: 'tone', label: 'Tone', type: 'text', description: 'Optional tone for the response (e.g., professional, friendly).' },
      { name: 'audience', label: 'Audience', type: 'text', description: 'Optional target audience for the response.' },
      { name: 'response_format', label: 'Response Format', type: 'text', description: 'Optional format for the response (e.g., summary, table).' },
    ],
    tcef: [
      { name: 'task', label: 'Task', type: 'textarea', description: 'Optional task description to clarify the action.' },
      { name: 'context', label: 'Context', type: 'textarea', description: 'Optional background context for the task.' },
      { name: 'example', label: 'Example', type: 'textarea', description: 'Optional example to guide the AI\'s response.' },
      { name: 'format', label: 'Format', type: 'text', description: 'Optional output format (e.g., table, list).' },
    ],
    crispe: [
      { name: 'role', label: 'Role', type: 'text', description: 'Optional role or expertise to assign to the AI (e.g., senior strategist).' },
      { name: 'insight', label: 'Insight', type: 'textarea', description: 'Optional focus area for deep analysis (e.g., data-driven insights).' },
      { name: 'style', label: 'Style', type: 'text', description: 'Optional style for the output (e.g., concise, detailed).' },
      { name: 'persona', label: 'Persona', type: 'text', description: 'Optional persona for the AI (e.g., pragmatic PM).' },
      { name: 'example', label: 'Example', type: 'textarea', description: 'Optional example to demonstrate the desired output.' },
    ],
    rtf: [
      { name: 'role', label: 'Role', type: 'text', description: 'Optional role for the AI (e.g., UX designer).' },
      { name: 'task', label: 'Task', type: 'textarea', description: 'Optional task description to define the action.' },
      { name: 'format', label: 'Format', type: 'text', description: 'Optional output format (e.g., step-by-step list, diagram).' },
    ],
    ice: [
      { name: 'instruction', label: 'Instruction', type: 'textarea', description: 'Optional clear instruction for the AI.' },
      { name: 'context', label: 'Context', type: 'textarea', description: 'Optional background context for the task.' },
      { name: 'example', label: 'Example', type: 'textarea', description: 'Optional example to guide the AI\'s response.' },
    ],
    craft: [
      { name: 'capability', label: 'Capability', type: 'text', description: 'Optional AI capability to leverage (e.g., data analysis).' },
      { name: 'role', label: 'Role', type: 'text', description: 'Optional role for the AI (e.g., data scientist).' },
      { name: 'action', label: 'Action', type: 'text', description: 'Optional specific action to perform.' },
      { name: 'format', label: 'Format', type: 'text', description: 'Optional output format (e.g., table, report).' },
      { name: 'tone', label: 'Tone', type: 'text', description: 'Optional tone for the response (e.g., technical, persuasive).' },
    ],
    ape: [
      { name: 'action', label: 'Action', type: 'text', description: 'Optional specific action to perform.' },
      { name: 'purpose', label: 'Purpose', type: 'textarea', description: 'Optional purpose or goal of the task.' },
      { name: 'expectation', label: 'Expectation', type: 'textarea', description: 'Optional expected output requirements (e.g., ranked list).' },
    ],
    pecra: [
      { name: 'purpose', label: 'Purpose', type: 'textarea', description: 'Optional goal of the task (e.g., persuade executives).' },
      { name: 'expectation', label: 'Expectation', type: 'textarea', description: 'Optional expected output (e.g., one-paragraph argument).' },
      { name: 'context', label: 'Context', type: 'textarea', description: 'Optional background context for the task.' },
      { name: 'request', label: 'Request', type: 'textarea', description: 'Optional specific request for the AI.' },
      { name: 'audience', label: 'Audience', type: 'text', description: 'Optional target audience (e.g., company founders).' },
    ],
    oscar: [
      { name: 'objective', label: 'Objective', type: 'textarea', description: 'Optional goal of the task (e.g., build an MVP).' },
      { name: 'scope', label: 'Scope', type: 'textarea', description: 'Optional boundaries of the task.' },
      { name: 'constraints', label: 'Constraints', type: 'textarea', description: 'Optional limits (e.g., budget, time).' },
      { name: 'assumptions', label: 'Assumptions', type: 'textarea', description: 'Optional assumptions for the task.' },
      { name: 'results', label: 'Results', type: 'textarea', description: 'Optional expected results (e.g., report with metrics).' },
    ],
    rasce: [
      { name: 'role', label: 'Role', type: 'text', description: 'Optional role for the AI (e.g., project management consultant).' },
      { name: 'action', label: 'Action', type: 'text', description: 'Optional specific action to perform.' },
      { name: 'steps', label: 'Steps (comma-separated)', type: 'text', description: 'Optional list of steps to break down the task.' },
      { name: 'constraints', label: 'Constraints', type: 'textarea', description: 'Optional constraints (e.g., time limits).' },
      { name: 'examples', label: 'Examples', type: 'textarea', description: 'Optional examples to guide the AI.' },
    ],
    reflection: [
      { name: 'review_criteria', label: 'Review Criteria', type: 'text', description: 'Optional criteria for self-assessment (e.g., clarity, accuracy).' },
    ],
    flipped_interaction: [
      { name: 'question_count', label: 'Question Count', type: 'number', description: 'Optional number of clarifying questions to ask (default: 5).' },
    ],
    bab: [
      { name: 'before', label: 'Before', type: 'textarea', description: 'Optional description of the current state.' },
      { name: 'after', label: 'After', type: 'textarea', description: 'Optional description of the desired state.' },
      { name: 'bridge', label: 'Bridge', type: 'textarea', description: 'Optional description of how to transition from current to desired state.' },
    ],
    prompt: [
      { name: 'context', label: 'Context', type: 'textarea', description: 'Optional background context for the task.' },
      { name: 'style', label: 'Style', type: 'text', description: 'Optional style for the response (e.g., bullet points, narrative).' },
      { name: 'tone', label: 'Tone', type: 'text', description: 'Optional tone for the response (e.g., professional, friendly).' },
      { name: 'audience', label: 'Audience', type: 'text', description: 'Optional target audience for the response.' },
      { name: 'response_format', label: 'Response Format', type: 'text', description: 'Optional format for the response (e.g., summary, table).' },
    ],
    soap: [
      { name: 'sections', label: 'Sections (comma-separated)', type: 'text', description: 'Optional sections to include in the SOAP response.' },
      { name: 'tone', label: 'Tone', type: 'text', description: 'Optional tone for the output (e.g., professional, concise).' },
      { name: 'format', label: 'Format', type: 'text', description: 'Optional output format (e.g., bullet points, paragraph).' },
    ],
    clear: [
      { name: 'steps', label: 'Steps', type: 'number', description: 'Optional number of steps to break down the task (default: 3).' },
      { name: 'style', label: 'Style', type: 'text', description: 'Optional style for presenting steps (e.g., numbered, bulleted).' },
      { name: 'audience', label: 'Audience', type: 'text', description: 'Optional target audience for the instructions.' },
    ],
    prism: [
      { name: 'perspectives', label: 'Perspectives', type: 'number', description: 'Optional number of perspectives to consider (default: 3).' },
      { name: 'focus_area', label: 'Focus Area', type: 'text', description: 'Optional specific focus area for analysis.' },
      { name: 'format', label: 'Format', type: 'text', description: 'Optional output format (e.g., table, bullet points).' },
    ],
    grips: [
      { name: 'granularity', label: 'Granularity', type: 'text', description: 'Optional granularity of the output (low, medium, high).' },
      { name: 'context', label: 'Context', type: 'textarea', description: 'Optional background context for the task.' },
      { name: 'examples', label: 'Examples', type: 'textarea', description: 'Optional examples to guide the AI\'s response.' },
    ],
    app: [
      { name: 'target_platform', label: 'Target Platform', type: 'text', description: 'Optional target platform for the app (e.g., web, mobile).' },
      { name: 'audience', label: 'Audience', type: 'text', description: 'Optional target audience for the app.' },
      { name: 'style', label: 'Style', type: 'text', description: 'Optional style for output messages or instructions.' },
    ],
    scope: [
      { name: 'boundaries', label: 'Boundaries', type: 'textarea', description: 'Optional boundaries for the task (e.g., time, budget, resources).' },
      { name: 'priority', label: 'Priority', type: 'text', description: 'Optional priority level of the task (e.g., high, medium, low).' },
      { name: 'outcome_focus', label: 'Outcome Focus', type: 'textarea', description: 'Optional expected outcome focus for the AI response.' },
    ],
    tool_oriented_prompting: [
      { name: 'tools', label: 'Tools (comma-separated)', type: 'text', description: 'Optional list of external tools to integrate with the prompt.' },
      { name: 'sequence', label: 'Sequence', type: 'textarea', description: 'Optional execution sequence for combining prompts and tools.' },
      { name: 'context', label: 'Context', type: 'textarea', description: 'Optional background context for tool usage.' },
    ],
    neuro_symbolic_prompting: [
      { name: 'logic_rules', label: 'Logic Rules', type: 'textarea', description: 'Optional symbolic logic rules to guide reasoning.' },
      { name: 'focus_area', label: 'Focus Area', type: 'text', description: 'Optional domain or topic for combining logic and LLM output.' },
      { name: 'explanation_depth', label: 'Explanation Depth', type: 'text', description: 'Optional level of explanation detail (low, medium, high).' },
    ],
    dynamic_context_windows: [
      { name: 'max_window_size', label: 'Max Window Size', type: 'number', description: 'Optional maximum token length for context windows.' },
      { name: 'prioritization_strategy', label: 'Prioritization Strategy', type: 'text', description: 'Optional strategy for prioritizing context (recent_first, important_first).' },
      { name: 'retain_history', label: 'Retain History', type: 'text', description: 'Whether to retain previous interactions in context (true/false).' },
    ],
    meta_cognitive_prompting: [
      { name: 'confidence_threshold', label: 'Confidence Threshold', type: 'number', description: 'Optional confidence threshold for self-reflection and output verification.' },
      { name: 'introspection_depth', label: 'Introspection Depth', type: 'text', description: 'Optional level of self-reflection detail (low, medium, high).' },
      { name: 'explanation_style', label: 'Explanation Style', type: 'text', description: 'Optional style for meta-cognitive explanations (concise, detailed).' },
    ],
    prompt_ensembles: [
      { name: 'strategies', label: 'Strategies (comma-separated)', type: 'text', description: 'Optional list of different prompting strategies to blend.' },
      { name: 'weightings', label: 'Weightings (comma-separated)', type: 'text', description: 'Optional weights for each strategy (must match the number of strategies).' },
      { name: 'output_combination_method', label: 'Combination Method', type: 'text', description: 'Optional method to combine outputs (majority_vote, average, weighted_average).' },
    ],
  };