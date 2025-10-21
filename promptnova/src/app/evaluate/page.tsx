"use client";

import React, { useState } from 'react';
import CryptoJS from 'crypto-js';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { EvaluateForm } from '@/components/evaluate/EvaluateForm';
import { EvaluateHero } from '@/components/evaluate/EvaluateHero';
import { EvaluateResultDisplay } from '@/components/evaluate/EvaluateResultDisplay';
import { Sidebar } from '@/components/Home/Sidebar';
import { RefreshCw, Eye, EyeOff } from 'lucide-react';


interface FullEvaluationResult {
  llm_as_judge: {
    clarity: number;
    specificity: number;
    context: number;
    goal_alignment: number;
    measurability: number;
    overall: number;
    comment: string;
  };
  t_rag: {
    intent_alignment: number;
    completeness: number;
    relevance: number;
    ambiguity: number;
    overall: number;
  };
  mar_framework: {
    clarity: number;
    completeness: number;
    relevance: number;
    structure: number;
    creativity_precision_balance: number;
    overall_score: number;
  };
  final_evaluation: {
    final_score: number;
    strengths: string;
    areas_for_improvement: string;
    report: string;
  };
}

const getCookie = (name: string): string | null => {
  if (typeof document === 'undefined') return null;
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
};

const getStorageKey = (model: string) => `${model}_api_key_encrypted`;

const EvaluatePage = () => {
  const [promptToEvaluate, setPromptToEvaluate] = useState('');
  const [initialPrompt, setInitialPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<FullEvaluationResult | null>(null);
  const [selectedModel, setSelectedModel] = useState('gemini');
  const [selectedGroqModel, setSelectedGroqModel] = useState('llama3-8b-8192');
  const [isReauthenticating, setIsReauthenticating] = useState(false);
  const [reauthPassword, setReauthPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!promptToEvaluate.trim()) {
      setError('Please enter a prompt to evaluate.');
      return;
    }

    const storageKey = getStorageKey(selectedModel);
    const passwordCookieName = `api_key_password_${selectedModel}`;

    const encryptedApiKey = localStorage.getItem(storageKey);
    const password = getCookie(passwordCookieName);

    if (encryptedApiKey && !password) {
      setIsReauthenticating(true);
      setError('Your session has expired. Please re-enter your password.');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt_to_evaluate: promptToEvaluate,
          initial_prompt: initialPrompt || null,
          selected_model: selectedModel,
          selected_groq_model: selectedGroqModel,
          api_key: encryptedApiKey,
          password: password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'An unknown error occurred.');
      }

      const data: FullEvaluationResult = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
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
    <div className="flex min-h-screen flex-col bg-white dark:bg-gray-900">
      <Navbar />
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
                    {error && <p className="text-red-500 dark:text-red-400 text-sm mb-4">{error}</p>}
                    <div className="flex justify-end gap-4">
                        <button type="button" onClick={() => setIsReauthenticating(false)} className="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-100 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">Cancel</button>
                        <button type="submit" disabled={isLoading} className="px-4 py-2 bg-gray-800 dark:bg-blue-600 text-white rounded-md flex items-center gap-2 disabled:bg-gray-400 dark:disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors">
                            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                            {isLoading ? 'Verifying...' : 'Confirm & Evaluate'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
      )}
      <div className="flex flex-1 flex-col md:flex-row">
        <Sidebar
          selectedModel={selectedModel}
          setSelectedModel={setSelectedModel}
          selectedGroqModel={selectedGroqModel}
          setSelectedGroqModel={setSelectedGroqModel}
        />
        <main className="flex-1 bg-gray-50 dark:bg-gray-800/50 p-6 md:p-10">
          <div className="mx-auto max-w-4xl">
            <EvaluateHero />
            <EvaluateForm
              promptToEvaluate={promptToEvaluate}
              setPromptToEvaluate={setPromptToEvaluate}
              initialPrompt={initialPrompt}
              setInitialPrompt={setInitialPrompt}
              handleSubmit={handleSubmit}
              isLoading={isLoading}
            />
            {error && !isReauthenticating && <div className="my-4 p-4 bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-500/30 rounded-md">{error}</div>}
            <EvaluateResultDisplay result={result} isLoading={isLoading} error={error} />
          </div>
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default EvaluatePage;