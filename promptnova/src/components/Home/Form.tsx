'use client'
import React, { useState, useEffect } from 'react';
import { Info, RefreshCw, Eye, EyeOff } from 'lucide-react';
import CryptoJS from 'crypto-js';
import { RefineForm } from './RefineForm';
import { AdvancedOptions } from './AdvancedOptions';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface Example {
  id: number;
  input: string;
  output: string;
}
interface FormProps {
  result: string;
  setResult: (result: string) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string) => void;
  isLoading: boolean;
  selectedModel: string;
  selectedGroqModel: string;
}

const getCookie = (name: string): string | null => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
};

const getStorageKey = (model: string) => `${model}_api_key_encrypted`;

const combos = [
  {
    name: "Custom",
    description: "Select your own combination of types and framework.",
    types: [] as string[],
    framework: null as string | null,
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
];


export const Form: React.FC<FormProps> = ({ result, setResult, setIsLoading, setError, isLoading, selectedModel, selectedGroqModel }) => {
  const types = [
    { name: 'Zero Shot', slug: 'zero_shot' },
    { name: 'One Shot', slug: 'one_shot' },
    { name: 'Chain of Thought (CoT)', slug: 'cot' },
    { name: 'Tree of Thought (ToT)', slug: 'tot' },
    { name: 'ReAct', slug: 'react' },
    { name: 'In Context', slug: 'in_context' },
    { name: 'Emotion', slug: 'emotion' },
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
    { name: 'Persona Switching', slug: 'persona_switching' },
    { name: 'Scaffolded Prompting', slug: 'scaffolded_prompting' },
    { name: 'Deliberation Prompting', slug: 'deliberation_prompting' },
    { name: 'Context Expansion', slug: 'context_expansion' },
    { name: 'Goal-Oriented Prompting', slug: 'goal_oriented_prompting' },
  ];

  const frameworks = [
    { name: 'Co-Star', slug: 'co_star' },
    { name: 'TCEF', slug: 'tcef' },
    { name: 'CRISPE', slug: 'crispe' },
    { name: 'RTF', slug: 'rtf' },
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
    { name: 'SOAP', slug: 'soap' },
    { name: 'CLEAR', slug: 'clear' },
    { name: 'PRISM', slug: 'prism' },
    { name: 'GRIPS', slug: 'grips' },
    { name: 'APP', slug: 'app' },
    { name: 'SCOPE', slug: 'scope' },
    { name: 'Tool-Oriented Prompting (TOP)', slug: 'tool_oriented_prompting' },
    { name: 'Neuro-Symbolic Prompting', slug: 'neuro_symbolic_prompting' },
    { name: 'Dynamic Context Windows', slug: 'dynamic_context_windows' },
    { name: 'Meta-Cognitive Prompting', slug: 'meta_cognitive_prompting' },
    { name: 'Prompt Ensembles', slug: 'prompt_ensembles' },
  ];

  const [promptText, setPromptText] = useState('');
  const [examples, setExamples] = useState<Example[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [selectedFramework, setSelectedFramework] = useState<string | null>(null);
  const [currentComboIndex, setCurrentComboIndex] = useState(0);
  const [showInfo, setShowInfo] = useState(false);
  const [showAllTypes, setShowAllTypes] = useState(false);
  const [showAllFrameworks, setShowAllFrameworks] = useState(false);
  const [showRefineModal, setShowRefineModal] = useState(false);
  const [isReauthenticating, setIsReauthenticating] = useState(false);
  const [reauthPassword, setReauthPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [parsedPrompt, setParsedPrompt] = useState('');
  const [mode, setMode] = useState<'normal' | 'expert'>('normal');
  const [advancedParams, setAdvancedParams] = useState<any>({ types: {}, framework: {} });
  const [showErrorDialog, setShowErrorDialog] = useState(false);
  const [errorDialogContent, setErrorDialogContent] = useState({ message: '', rawResponse: '' });

  const visibleTypes = showAllTypes ? types : types.slice(0, 6);
  const visibleFrameworks = showAllFrameworks ? frameworks : frameworks.slice(0, 6);

  useEffect(() => {
    const handleShowRefineModal = () => setShowRefineModal(true);
    window.addEventListener('show-refine-modal', handleShowRefineModal);
    return () => {
      window.removeEventListener('show-refine-modal', handleShowRefineModal);
    };
  }, []);

  useEffect(() => {
    const matchingComboIndex = combos.findIndex((combo, index) => {
      if (index === 0) return false; // Skip "Custom"
      const sortedComboTypes = [...combo.types].sort();
      const sortedCurrentTypes = [...selectedTypes].sort();
      
      const typesMatch = sortedComboTypes.length === sortedCurrentTypes.length && 
                         sortedComboTypes.every((t, i) => t === sortedCurrentTypes[i]);
      
      const frameworkMatch = combo.framework === selectedFramework;
      
      return typesMatch && frameworkMatch;
    });

    const newIndex = matchingComboIndex === -1 ? 0 : matchingComboIndex;
    if (newIndex !== currentComboIndex) {
      setCurrentComboIndex(newIndex);
    }
  }, [selectedTypes, selectedFramework, currentComboIndex]);

  useEffect(() => {
    if (result) {
      const explanationSeparator = "**Explanation of Improvements and Rationale:**";
      const promptSeparator = "**Refined Prompt:**";
      
      let promptPart = result;

      if (result.includes(explanationSeparator)) {
        const parts = result.split(explanationSeparator);
        promptPart = parts[0];
      }

      if (promptPart.includes(promptSeparator)) {
        promptPart = promptPart.split(promptSeparator)[1];
      }
      
      const startIndex = promptPart.indexOf('```');
      const endIndex = promptPart.lastIndexOf('```');
      let cleanedPrompt;
      if (startIndex !== -1 && endIndex > startIndex) {
        cleanedPrompt = promptPart.substring(startIndex + 3, endIndex).replace(/^[a-zA-Z]*\n?/, '').trim();
      } else {
        cleanedPrompt = promptPart.trim();
      }
      
      setParsedPrompt(cleanedPrompt);
    } else {
      setParsedPrompt('');
    }
  }, [result]);

  const handleTypeToggle = (slug: string) => {
    setSelectedTypes(prev =>
      prev.includes(slug) ? prev.filter(s => s !== slug) : [...prev, slug]
    );
  };

  const handleFrameworkSelect = (slug: string) => {
    setSelectedFramework(prev => (prev === slug ? null : slug));
  };

  const handleNextCombo = () => {
    const nextIndex = (currentComboIndex + 1) % combos.length;
    const selectedCombo = combos[nextIndex];
    
    setCurrentComboIndex(nextIndex);
    setSelectedTypes(selectedCombo.types);
    setSelectedFramework(selectedCombo.framework);
  };

  const handleRemoveSelected = (slug: string, type: 'type' | 'framework') => {
    if (type === 'type') {
      setSelectedTypes(prev => prev.filter(s => s !== slug));
    } else {
      setSelectedFramework(null);
    }
  };

  const addExample = () => {
    setExamples(prev => [...prev, { id: Date.now(), input: '', output: '' }]);
  };

  const handleExampleChange = (id: number, field: 'input' | 'output', value: string) => {
    setExamples(prev => prev.map(ex => ex.id === id ? { ...ex, [field]: value } : ex));
  };

  const removeExample = (id: number) => {
    setExamples(prev => prev.filter(ex => ex.id !== id));
  };


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const storageKey = getStorageKey(selectedModel);
    const passwordCookieName = `api_key_password_${selectedModel}`;

    const encryptedApiKey = localStorage.getItem(storageKey);
    const password = getCookie(passwordCookieName);

    if (encryptedApiKey && !password) {
      setIsReauthenticating(true);
      setResult('');
      setIsLoading(false);
      return;
    }

    let finalPromptText = promptText;

    if (mode === 'expert') {
      const cleanParams: any = { types: {}, framework: {} };

      Object.entries(advancedParams.types).forEach(([type, params]: [string, any]) => {
        const cleanTypeParams = Object.fromEntries(Object.entries(params).filter(([_, v]) => v));
        if (Object.keys(cleanTypeParams).length > 0) {
          cleanParams.types[type] = cleanTypeParams;
        }
      });

      if (advancedParams.framework) {
        const frameworkSlug = Object.keys(advancedParams.framework)[0];
        if (frameworkSlug) {
          const frameworkParams = advancedParams.framework[frameworkSlug];
          const cleanFrameworkParams = Object.fromEntries(Object.entries(frameworkParams).filter(([_, v]) => v));
          if (Object.keys(cleanFrameworkParams).length > 0) {
            cleanParams.framework[frameworkSlug] = cleanFrameworkParams;
          }
        }
      }
      
      const hasExpertData = Object.keys(cleanParams.types).length > 0 || Object.keys(cleanParams.framework).length > 0;

      if (hasExpertData) {
        const expertDetailsString = `Expert Details:\n${JSON.stringify(cleanParams, null, 2)}`;
        finalPromptText = `${expertDetailsString}\n\n---\n\n${promptText}`;
      }
    }

    const payload = {
      user_input: finalPromptText,
      examples: examples.map(({ id, ...rest }) => rest).filter(ex => ex.input && ex.output),
      style: selectedTypes,
      framework: selectedFramework,
      api_key: encryptedApiKey,
      password: password,
      selected_model: selectedModel,
      selected_groq_model: selectedGroqModel,
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/refine', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: `HTTP error! status: ${response.status}` }));
        let errorMessage = errorData.detail;

        if (Array.isArray(errorMessage)) {
          errorMessage = errorMessage
            .map((err: any) => {
              const loc = err.loc?.join(' > ') || 'N/A';
              const msg = err.msg || 'Unknown error';
              return `${msg} (at: ${loc})`;
            })
            .join('\n');
        }

        throw new Error(String(errorMessage) || 'An unknown error occurred.');
      }

      const data = await response.json();
      if (data.output_str) {
        try {
          const parsedOutput = JSON.parse(data.output_str);
          if (parsedOutput.error === 'parsing_failed') {
            setErrorDialogContent({
              message: parsedOutput.message,
              rawResponse: parsedOutput.raw_response,
            });
            setShowErrorDialog(true);
            setResult(parsedOutput.raw_response); // Show raw response in the background
          } else {
            setResult(data.output_str);
          }
        } catch (e) {
          // Not a JSON string, so it's a valid raw response
          setResult(data.output_str);
        }
      } else {
        setError("Received an unexpected response format from the server.");
        console.error("Unexpected response:", data);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'An unknown error occurred.');
      setResult('');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReauthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reauthPassword) {
        setError('Password cannot be empty.');
        return;
    }
    setIsLoading(true);
    setError('');

    const storageKey = getStorageKey(selectedModel);
    const encryptedKey = localStorage.getItem(storageKey);
    if (!encryptedKey) {
        setError("Encrypted key not found. Please save it again in Settings.");
        setIsLoading(false);
        return;
    }

    try {
        const decryptedBytes = CryptoJS.AES.decrypt(encryptedKey, reauthPassword);
        const decryptedKey = decryptedBytes.toString(CryptoJS.enc.Utf8);

        if (!decryptedKey) {
            throw new Error('Incorrect password.');
        }

        const passwordCookieName = `api_key_password_${selectedModel}`;
        document.cookie = `${passwordCookieName}=${reauthPassword};max-age=${7 * 24 * 60 * 60};path=/;SameSite=Lax`;
        
        setIsReauthenticating(false);
        setReauthPassword('');
        await handleSubmit(e);

    } catch (err) {
        setError("Decryption failed. Incorrect password.");
        setIsLoading(false);
    }
  };

  return (
    <div className="p-8 bg-gray-50 dark:bg-gray-900/50 rounded-lg shadow-md max-w-3xl mx-auto my-8 border border-gray-200 dark:border-gray-800">
      <AlertDialog open={showErrorDialog} onOpenChange={setShowErrorDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Parsing Error</AlertDialogTitle>
            <AlertDialogDescription>
              {errorDialogContent.message}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-md max-h-60 overflow-y-auto">
            <pre className="text-xs text-gray-600 dark:text-gray-400 whitespace-pre-wrap">
              <code>{errorDialogContent.rawResponse}</code>
            </pre>
          </div>
          <AlertDialogFooter>
            <AlertDialogCancel>Close</AlertDialogCancel>
            <AlertDialogAction onClick={() => {
              setPromptText(errorDialogContent.rawResponse);
              setShowErrorDialog(false);
            }}>Use Raw Text</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {isReauthenticating && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" onClick={() => setIsReauthenticating(false)}>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl p-6 max-w-xl w-full" onClick={e => e.stopPropagation()}>
                <h2 className="text-2xl font-bold mb-2 text-gray-800 dark:text-gray-100">Session Expired</h2>
                <p className="text-gray-600 dark:text-gray-400 mb-4 text-sm">Please re-enter your password to continue.</p>
                <form onSubmit={handleReauthSubmit}>
                    <div className="mb-4">
                        <label htmlFor="reauth-password-form" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Password</label>
                        <div className="relative">
                            <input id="reauth-password-form" type={showPassword ? 'text' : 'password'} value={reauthPassword} onChange={(e) => setReauthPassword(e.target.value)} className="w-full p-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500" placeholder="Enter password" autoFocus />
                            <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200">
                                {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />} 
                            </button>
                        </div>
                    </div>
                    <div className="flex justify-end gap-4">
                        <button type="button" onClick={() => setIsReauthenticating(false)} className="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-100 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">Cancel</button>
                        <button type="submit" disabled={isLoading} className="px-4 py-2 bg-gray-800 dark:bg-blue-600 text-white rounded-md flex items-center gap-2 disabled:bg-gray-400 dark:disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors">
                            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                            {isLoading ? 'Verifying...' : 'Confirm & Generate'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
      )}
      {showRefineModal && <RefineForm 
        originalPrompt={promptText} 
        finalPrompt={parsedPrompt} 
        onClose={() => setShowRefineModal(false)} 
        onRefined={(newPrompt) => { setResult(newPrompt); }}
        style={selectedTypes}
        framework={selectedFramework}
        selectedModel={selectedModel}
        selectedGroqModel={selectedGroqModel}
      />}
      <form onSubmit={handleSubmit}>
        <div className="flex justify-center mb-6">
          <div className="bg-gray-200 dark:bg-gray-800 p-1 rounded-lg flex">
            <button
              type="button"
              onClick={() => setMode('normal')}
              className={`px-6 py-2 text-sm font-medium rounded-md transition-colors ${
                mode === 'normal' ? 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 shadow' : 'text-gray-600 dark:text-gray-400'
              }`}
            >
              Normal
            </button>
            <button
              type="button"
              onClick={() => setMode('expert')}
              className={`px-6 py-2 text-sm font-medium rounded-md transition-colors ${
                mode === 'expert' ? 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 shadow' : 'text-gray-600 dark:text-gray-400'
              }`}
            >
              Expert
            </button>
          </div>
        </div>
        <div className="mb-6">
          <label htmlFor="prompt-input" className="block text-gray-700 dark:text-gray-300 text-sm font-semibold mb-2">
            Enter Your Prompt
          </label>
          <textarea
            id="prompt-input"
            className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 resize-y min-h-[120px]"
            value={promptText}
            onChange={(e) => setPromptText(e.target.value)}
            placeholder="e.g., Generate a Python function to calculate Fibonacci sequence."
          />
        </div>

        {mode === 'expert' && (
          <AdvancedOptions
            selectedTypes={selectedTypes}
            selectedFramework={selectedFramework}
            advancedParams={advancedParams}
            setAdvancedParams={setAdvancedParams}
          />
        )}

        <div className="mb-6">
          <label className="block text-gray-700 dark:text-gray-300 text-sm font-semibold mb-3">
            Examples (Optional)
          </label>
          <div className="space-y-4">
            {examples.map((example, index) => (
              <div key={example.id} className="relative rounded-md border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4">
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  <div>
                    <label htmlFor={`example-input-${index}`} className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                      Input
                    </label>
                    <textarea
                      id={`example-input-${index}`}
                      value={example.input}
                      onChange={(e) => handleExampleChange(example.id, 'input', e.target.value)}
                      placeholder="Example input"
                      className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-400 bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 resize-y min-h-[80px] text-sm"
                    />
                  </div>
                  <div>
                    <label htmlFor={`example-output-${index}`} className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
                      Output/Example
                    </label>
                    <textarea
                      id={`example-output-${index}`}
                      value={example.output}
                      onChange={(e) => handleExampleChange(example.id, 'output', e.target.value)}
                      placeholder="Expected output"
                      className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-400 bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 resize-y min-h-[80px] text-sm"
                    />
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => removeExample(example.id)}
                  className="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-gray-500 dark:bg-gray-600 text-white hover:bg-red-600 dark:hover:bg-red-500 transition-colors"
                  aria-label="Remove example"
                >
                  <span className="text-sm leading-none pb-0.5">&times;</span>
                </button>
              </div>
            ))}
          </div>
          <button type="button" onClick={addExample} className="mt-4 w-full rounded-md border-2 border-dashed border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 py-2 px-4 text-center text-sm font-medium text-gray-600 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
            + Add Example
          </button>
        </div>

        <div className="mb-6">
          <h2 className="text-gray-700 dark:text-gray-300 text-sm font-semibold mb-3">
            Prompt Strategy (Optional)
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">Select a pre-built strategy or create your own custom combination below.</p>
          <div className="relative flex items-center gap-2">
            <button
              type="button"
              onClick={handleNextCombo}
              className="flex-grow bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-800 dark:text-gray-200 px-4 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-left"
            >
              <span className="font-medium">{combos[currentComboIndex].name}</span>
            </button>
            {currentComboIndex > 0 && (
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); setShowInfo(true); }}
                className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
                aria-label="Show strategy info"
              >
                <Info className="h-5 w-5" />
              </button>
            )}
          </div>
        </div>

        {showInfo && currentComboIndex > 0 && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={() => setShowInfo(false)}>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 max-w-md w-full" onClick={e => e.stopPropagation()}>
              <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 mb-2">{combos[currentComboIndex].name}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">{combos[currentComboIndex].description}</p>
              <button onClick={() => setShowInfo(false)} className="mt-4 w-full bg-gray-800 dark:bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 dark:hover:bg-blue-700">Close</button>
            </div>
          </div>
        )}

        <div className="mb-6">
          <h2 className="text-gray-700 dark:text-gray-300 text-sm font-semibold mb-3">Select Prompt Types (Multiple)</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {visibleTypes.map(type => (
              <button
                key={type.slug}
                type="button"
                onClick={() => handleTypeToggle(type.slug)}
                className={`px-4 py-2 rounded-md text-sm font-medium  transition-colors duration-200
                  ${selectedTypes.includes(type.slug) ?
                    'bg-gray-800 text-white dark:bg-gray-300 dark:text-gray-800 border border-gray-800 dark:border-white'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
              >
                {type.name}
              </button>
            ))}
          </div>
          {types.length > 6 && (
            <div className="mt-4 flex justify-center">
              <button
                type="button"
                onClick={() => setShowAllTypes(prev => !prev)}
                className="text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:underline"
              >
                {showAllTypes ? 'Show Less' : `Show ${types.length - 6} More...`}
              </button>
            </div>
          )}
        </div>

        <div className="mb-6">
          <h2 className="text-gray-700 dark:text-gray-300 text-sm font-semibold mb-3">Select Framework (Single)</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {visibleFrameworks.map(framework => (
              <button
                key={framework.slug}
                type="button"
                onClick={() => handleFrameworkSelect(framework.slug)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200
                  ${selectedFramework === framework.slug ?
                    'bg-gray-800 text-white dark:bg-gray-300 dark:text-gray-800 border border-gray-800 dark:border-white'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
              >
                {framework.name}
              </button>
            ))}
          </div>
          {frameworks.length > 6 && (
            <div className="mt-4 flex justify-center">
              <button
                type="button"
                onClick={() => setShowAllFrameworks(prev => !prev)} className="text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:underline"
              >
                {showAllFrameworks ? 'Show Less' : `Show ${frameworks.length - 6} More...`}
              </button>
            </div>
          )}
        </div>

        <div className="mb-6">
          <h2 className="text-gray-700 dark:text-gray-300 text-sm font-semibold mb-3">Selected Types</h2>
          <div className="flex flex-wrap gap-2">
            {selectedTypes.length > 0 ? (
              selectedTypes.map(slug => (
                <span key={slug} className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-full flex items-center gap-1 text-sm">
                  {types.find(t => t.slug === slug)?.name || slug}
                  <button
                    type="button"
                    onClick={() => handleRemoveSelected(slug, 'type')}
                    className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white ml-1"
                  >
                    &times;
                  </button>
                </span>
              ))
            ) : (
              <p className="text-gray-500 dark:text-gray-400 text-sm">No types selected.</p>
            )}
          </div>
        </div>

        <div className="mb-6">
          <h2 className="text-gray-700 dark:text-gray-300 text-sm font-semibold mb-3">Selected Framework</h2>
          <div className="flex flex-wrap gap-2">
            {selectedFramework ? (
              <span className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-full flex items-center gap-1 text-sm">
                {frameworks.find(f => f.slug === selectedFramework)?.name || selectedFramework}
                <button
                  type="button"
                  onClick={() => handleRemoveSelected(selectedFramework, 'framework')}
                  className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white ml-1"
                >
                  &times;
                </button>
              </span>
            ) : (
              <p className="text-gray-500 dark:text-gray-400 text-sm">No framework selected.</p>
            )}
          </div>
        </div>

        <button
          type="submit"
          className="w-full bg-gray-800 text-white dark:bg-gray-300 dark:text-gray-800 px-6 py-3 rounded-md hover:bg-gray-700 dark:hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 font-semibold text-lg disabled:bg-gray-400 dark:disabled:bg-gray-500 disabled:cursor-not-allowed"
          disabled={isLoading}
        >
          {isLoading ? 'Generating...' : 'Generate Prompt'}
        </button>
      </form>

    </div>
  )
}
