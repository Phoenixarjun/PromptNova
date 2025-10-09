'use client'
import React, { useState, useEffect } from 'react';
import { Info, RefreshCw, Eye, EyeOff, Settings, Check, Sparkles, WandSparkles } from 'lucide-react';
import CryptoJS from 'crypto-js';
import { RefineForm } from './RefineForm';
import { AdvancedOptions } from './AdvancedOptions';
import {
  combos,
  types,
  frameworks,
  projectParamsSchema,
  Example,
  AdvancedParams,
  ValidationError,
} from '../../data/formConstants';
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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

interface ProjectParams {
  [key: string]: string;
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

export const Form: React.FC<FormProps> = ({ result, setResult, setIsLoading, setError, isLoading, selectedModel, selectedGroqModel }) => {
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
  const [settingMode, setSettingMode] = useState<'default' | 'expert' | 'expert+'>('default');
  const [promptMode, setPromptMode] = useState<'task' | 'project'>('task');
  const [projectParams, setProjectParams] = useState<ProjectParams>({});
  const [advancedParams, setAdvancedParams] = useState<AdvancedParams>({ types: {}, framework: {} });
  const [showErrorDialog, setShowErrorDialog] = useState(false);
  const [errorDialogContent, _setErrorDialogContent] = useState({ message: '', rawResponse: '' });
  const [isPicking, setIsPicking] = useState(false);
  const [autoSelectMessage, setAutoSelectMessage] = useState<string | null>(null);

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
    if (settingMode === 'default') {
      const defaultCombo = combos.find(c => c.name === "Universal Adaptive Engine") || combos[1];
      setSelectedTypes(defaultCombo.types);
      setSelectedFramework(defaultCombo.framework);
      setCurrentComboIndex(combos.indexOf(defaultCombo));
    } else {
      const matchingComboIndex = combos.findIndex((combo, index) => {
        if (index === 0) return false;
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
    }
  }, [selectedTypes, selectedFramework, currentComboIndex, settingMode]);

  useEffect(() => {
    if (result) {
      try {
        const parsed = JSON.parse(result);
        if (parsed && parsed.refined_prompt) {
          setParsedPrompt(parsed.refined_prompt);
        } else {
          setParsedPrompt(result); // Fallback to raw string
        }
      } catch {
        setParsedPrompt(result); // Fallback if not JSON
      }
    } else {
      setParsedPrompt('');
    }
  }, [result]);

  const handleTypeToggle = (slug: string) => {
    setAutoSelectMessage(null);
    setSelectedTypes(prev =>
      prev.includes(slug) ? prev.filter(s => s !== slug) : [...prev, slug]
    );
  };

  const handleFrameworkSelect = (slug: string) => {
    setAutoSelectMessage(null);
    setSelectedFramework(prev => (prev === slug ? null : slug));
  };

  const handleNextCombo = () => {
    const nextIndex = (currentComboIndex + 1) % combos.length;
    const selectedCombo = combos[nextIndex];
    
    setCurrentComboIndex(nextIndex);
    setAutoSelectMessage(null);
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

  const handleProjectParamsChange = (field: keyof ProjectParams, value: string) => {
    setProjectParams(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handlePickAgent = async () => {
    if (!promptText.trim()) {
      setError('Please enter a prompt first.');
      return;
    }
    setIsPicking(true);
    setError('');

    const storageKey = getStorageKey(selectedModel);
    const passwordCookieName = `api_key_password_${selectedModel}`;

    const encryptedApiKey = localStorage.getItem(storageKey);
    const password = getCookie(passwordCookieName);

    if (encryptedApiKey && !password) {
      setIsReauthenticating(true);
      setIsPicking(false);
      return;
    }

    const payload = {
      user_input: promptText,
      examples: examples.map(ex => ({ input: ex.input, output: ex.output })).filter(ex => ex.input && ex.output),
      api_key: encryptedApiKey,
      password: password,
      selected_model: selectedModel,
      selected_groq_model: selectedGroqModel,
    };

    try {
      const response = await fetch('https://promptnova.onrender.com/pick_agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get suggestions.');
      }
      const data = await response.json();
      const selectedTypeNames = (data.types || []).map((slug: string) => types.find(t => t.slug === slug)?.name || slug);
      const frameworkName = frameworks.find(f => f.slug === data.framework)?.name || data.framework;

      if (selectedTypeNames.length > 0 && frameworkName) {
        setAutoSelectMessage(`AI selected: ${selectedTypeNames.join(', ')} with the ${frameworkName} framework.`);
      }
      setSelectedTypes(data.types || []);
      setSelectedFramework(data.framework || null);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'An unknown error occurred.');
    } finally {
      setIsPicking(false);
    };
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
    let endpoint = 'https://promptnova.onrender.com/refine';

    if (settingMode === 'expert+') {
      const cleanParams: AdvancedParams = { types: {}, framework: {} };

      if (advancedParams.types) {
        Object.entries(advancedParams.types).forEach(([type, params]) => {
          const cleanTypeParams = Object.fromEntries(Object.entries(params).filter(([, v]) => v));
          if (Object.keys(cleanTypeParams).length > 0 && cleanParams.types) {
            cleanParams.types[type] = cleanTypeParams;
          }
        });
      }

      if (advancedParams.framework) {
        const frameworkSlug = Object.keys(advancedParams.framework)[0];
        if (frameworkSlug) {
          const frameworkParams = advancedParams.framework[frameworkSlug];
          const cleanFrameworkParams = Object.fromEntries(Object.entries(frameworkParams).filter(([, v]) => v));
          if (Object.keys(cleanFrameworkParams).length > 0 && cleanParams.framework) {
            cleanParams.framework[frameworkSlug] = cleanFrameworkParams;
          }
        }
      }
      
      const hasExpertData = (cleanParams.types && Object.keys(cleanParams.types).length > 0) || (cleanParams.framework && Object.keys(cleanParams.framework).length > 0);

      if (hasExpertData) {
        const expertDetailsString = `Expert Details:\n${JSON.stringify(cleanParams, null, 2)}`;
        finalPromptText = `${expertDetailsString}\n\n---\n\n${promptText}`;
      }
    }

    if (promptMode === 'project') {
      endpoint = 'https://promptnova.onrender.com/project';
      if (settingMode === 'expert+') {
        const cleanProjectParams = Object.fromEntries(Object.entries(projectParams).filter(([, v]) => v));
        finalPromptText = `Project Details:\n${JSON.stringify(cleanProjectParams, null, 2)}\n\n---\n\n${promptText}`;
      }
    }

    if (selectedModel === 'groq') {
      finalPromptText += "\n\n---\nInstruction: For better clarity, your entire response must be a single, raw JSON object. Do not use tools, functions, or markdown formatting like ```json. Your output should start with { and end with }.";
    }
    
    const payload = {
      user_input: finalPromptText,
      examples: examples.map(ex => ({ input: ex.input, output: ex.output })).filter(ex => ex.input && ex.output),
      style: selectedTypes,
      framework: selectedFramework,
      api_key: encryptedApiKey,
      password: password,
      selected_model: selectedModel,
      selected_groq_model: selectedGroqModel,
    };

    if (promptMode === 'project') {
      payload.framework = 'co_star'; 
      payload.style = ['zero_shot']; 
    }

    try {
      const response = await fetch(endpoint, {

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
            .map((err: ValidationError) => {
              const loc = err.loc?.join(' > ') || 'N/A';
              const msg = err.msg || 'Unknown error';
              return `${msg} (at: ${loc})`;
            })
            .join('\n');
        }

        throw new Error(String(errorMessage) || 'An unknown error occurred.');
      }

      const data = await response.json();
      console.log(data);

      if (data) {
        if (promptMode === 'project') {
          setResult(JSON.stringify(data));
        } else if (data.output_str && typeof data.output_str === 'object') {
          setResult(JSON.stringify(data.output_str));
        } else {
          setResult(JSON.stringify({ refined_prompt: data.refined_prompt || data.updated_prompt, explanation: data.explanation || '' }));
        }
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

    } catch {
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
        promptMode={promptMode}
      />}
      <form onSubmit={handleSubmit}>
        <div className="relative flex justify-center items-center mb-6">
          <div className="flex-1 flex justify-center">
            <div className="bg-gray-200 dark:bg-gray-800 p-1 rounded-lg flex">
              <button type="button" onClick={() => setPromptMode('task')} className={`px-6 py-2 text-sm font-medium rounded-md transition-colors ${promptMode === 'task' ? 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 shadow' : 'text-gray-600 dark:text-gray-400'}`}>
                Task
              </button>
              <button type="button" onClick={() => setPromptMode('project')} className={`px-6 py-2 text-sm font-medium rounded-md transition-colors ${promptMode === 'project' ? 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 shadow' : 'text-gray-600 dark:text-gray-400'}`}>
                Project
              </button>
            </div>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button type="button" className="p-2 text-gray-500 rounded-full dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-700" aria-label="Settings">
                <Settings className="h-5 w-5" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuRadioGroup value={settingMode} onValueChange={(value) => setSettingMode(value as 'default' | 'expert' | 'expert+')}>
                <DropdownMenuRadioItem value="default">Default</DropdownMenuRadioItem>
                <DropdownMenuRadioItem value="expert">Expert</DropdownMenuRadioItem>
                <DropdownMenuRadioItem value="expert+">Expert +</DropdownMenuRadioItem>
              </DropdownMenuRadioGroup>
            </DropdownMenuContent>
          </DropdownMenu>
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
          <div className="mt-2 flex justify-end">
            <button type="button" onClick={handlePickAgent} disabled={isPicking} className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-md border transition-colors shadow-sm disabled:opacity-60 disabled:cursor-not-allowed bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700">
              {isPicking ? (
                <WandSparkles className="h-4 w-4 animate-pulse" />
              ) : (
                <Sparkles className="h-4 w-4" />
              )}
              {isPicking ? 'Thinking...' : 'Auto-Select Strategy'}
            </button>
          </div>
        </div>

        {promptMode === 'task' && settingMode === 'default' && (
          <div className={`p-4 my-6 text-sm text-center rounded-lg border transition-colors duration-300 ${
            autoSelectMessage
              ? 'text-green-700 bg-green-100 border-green-200 dark:bg-green-900/20 dark:text-green-300 dark:border-green-500/30'
              : 'text-blue-700 bg-blue-100 border-blue-200 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-500/30'
          }`}>
            {autoSelectMessage ? (
              <>
                <p className="font-semibold">Strategy Auto-Selected!</p>
                <p className="mt-1">{autoSelectMessage}</p>
              </>
            ) : (
              <>
                <p className="font-semibold">Current Mode: Default</p>
                <p className="mt-1">
                  Using the "{combos.find(c => c.name === "Universal Adaptive Engine")?.name || combos[1].name}" strategy. 
                  Switch to Expert or Expert+ via the settings icon for more options.
                </p>
              </>
            )}
          </div>
        )}

        {/* Scenarios for Expert and Expert+ modes */}
        {(settingMode === 'expert' || settingMode === 'expert+') && promptMode === 'task' && (
          <>
            {settingMode === 'expert+' && (
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
                  <div key={example.id} className="relative p-4 bg-white border border-gray-200 rounded-md dark:bg-gray-800 dark:border-gray-700">
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
                          className="w-full p-2 text-sm bg-white border border-gray-300 rounded-md resize-y min-h-[80px] focus:outline-none focus:ring-2 focus:ring-gray-400 dark:bg-gray-700 dark:border-gray-600 text-gray-800 dark:text-gray-200"
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
                          className="w-full p-2 text-sm bg-white border border-gray-300 rounded-md resize-y min-h-[80px] focus:outline-none focus:ring-2 focus:ring-gray-400 dark:bg-gray-700 dark:border-gray-600 text-gray-800 dark:text-gray-200"
                        />
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={() => removeExample(example.id)}
                      className="absolute flex items-center justify-center w-5 h-5 text-white transition-colors bg-gray-500 rounded-full -top-2 -right-2 hover:bg-red-600 dark:bg-gray-600 dark:hover:bg-red-500"
                      aria-label="Remove example"
                    >
                      <span className="text-sm leading-none pb-0.5">&times;</span>
                    </button>
                  </div>
                ))}
              </div>
              <button type="button" onClick={addExample} className="w-full px-4 py-2 mt-4 text-sm font-medium text-center text-gray-600 transition-colors bg-gray-50 border-2 border-dashed border-gray-300 rounded-md dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 hover:border-gray-400 hover:bg-gray-100 dark:hover:border-gray-600 dark:hover:bg-gray-700">
                + Add Example
              </button>
            </div>

            <div className="mb-6">
              <h2 className="mb-3 text-sm font-semibold text-gray-700 dark:text-gray-300">
                Prompt Strategy (Optional)
              </h2>
              <p className="mb-3 text-sm text-gray-500 dark:text-gray-400">Select a pre-built strategy or create your own custom combination below.</p>
              <div className="relative flex items-center gap-2">
                <button
                  type="button"
                  onClick={handleNextCombo}
                  className="flex-grow px-4 py-2 text-left text-gray-800 transition-colors bg-white border border-gray-300 rounded-md dark:bg-gray-800 dark:border-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <span className="font-medium">{combos[currentComboIndex].name}</span>
                </button>
                {currentComboIndex > 0 && (
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); setShowInfo(true); }}
                    className="p-2 text-gray-500 rounded-full dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-700"
                    aria-label="Show strategy info"
                  >
                    <Info className="h-5 w-5" />
                  </button>
                )}
              </div>
            </div>

            {showInfo && currentComboIndex > 0 && (
              <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50" onClick={() => setShowInfo(false)}>
                <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-xl dark:bg-gray-800" onClick={e => e.stopPropagation()}>
                  <h3 className="mb-2 text-lg font-bold text-gray-900 dark:text-gray-100">{combos[currentComboIndex].name}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{combos[currentComboIndex].description}</p>
                  <button onClick={() => setShowInfo(false)} className="w-full px-4 py-2 mt-4 text-white bg-gray-800 rounded-md dark:bg-blue-600 hover:bg-gray-700 dark:hover:bg-blue-700">Close</button>
                </div>
              </div>
            )}

            <div className="mb-6">
              <h2 className="mb-3 text-sm font-semibold text-gray-700 dark:text-gray-300">Select Prompt Types (Multiple)</h2>
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
              <h2 className="mb-3 text-sm font-semibold text-gray-700 dark:text-gray-300">Select Framework (Single)</h2>
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
              <h2 className="mb-3 text-sm font-semibold text-gray-700 dark:text-gray-300">Selected Types</h2>
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
                  <p className="text-sm text-gray-500 dark:text-gray-400">No types selected.</p>
                )}
              </div>
            </div>

            <div className="mb-6">
              <h2 className="mb-3 text-sm font-semibold text-gray-700 dark:text-gray-300">Selected Framework</h2>
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
                  <p className="text-sm text-gray-500 dark:text-gray-400">No framework selected.</p>
                )}
              </div>
            </div>
          </>
        )}

        {/* Scenario 3: Normal + Project */}
        {promptMode === 'project' && (settingMode === 'default' || settingMode === 'expert') && (
          <div className="p-4 my-6 text-sm text-center text-blue-700 bg-blue-100 border border-blue-200 rounded-lg dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-500/30">
            <p>For Project mode, the prompt will be automatically structured as JSON. Just describe your project requirements above.</p>
          </div>
        )}

        {/* Scenario 4: Expert + Project */}
        {promptMode === 'project' && settingMode === 'expert+' && (
          <div className="mb-6 space-y-4">
            <h2 className="mb-3 text-sm font-semibold text-gray-700 dark:text-gray-300">Project Details</h2>
            {Object.entries(projectParamsSchema).map(([key, { label, description }]) => (
              <div key={key}>
                <label htmlFor={`project-${key}`} className="block mb-1 text-xs font-medium text-gray-600 dark:text-gray-400">{label}</label>
                <textarea
                  id={`project-${key}`}
                  value={projectParams[key as keyof ProjectParams] || ''}
                  onChange={(e) => handleProjectParamsChange(key as keyof ProjectParams, e.target.value)}
                  placeholder={description}
                  className="w-full p-2 text-sm bg-white border border-gray-300 rounded-md resize-y min-h-[40px] focus:outline-none focus:ring-2 focus:ring-gray-400 dark:bg-gray-700 dark:border-gray-600 text-gray-800 dark:text-gray-200"
                  rows={1}
                />
              </div>
            ))}
          </div>
        )}

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
