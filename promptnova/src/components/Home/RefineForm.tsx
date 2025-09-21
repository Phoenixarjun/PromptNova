"use client"
import React, { useState } from 'react';
import { RefreshCw, Eye, EyeOff } from 'lucide-react';
import CryptoJS from 'crypto-js';

interface RefineFormProps {
  originalPrompt: string;
  finalPrompt: string;
  onClose: () => void;
  onRefined: (newPrompt: string) => void;
  style: string[];
  framework: string | null;
  selectedModel: string;
  selectedGroqModel: string;
}

const getCookie = (name: string): string | null => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
  return null;
};

export const RefineForm: React.FC<RefineFormProps> = ({ originalPrompt, finalPrompt, onClose, onRefined, style, framework, selectedModel, selectedGroqModel }) => {
  const [feedback, setFeedback] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isReauthenticating, setIsReauthenticating] = useState(false);
  const [reauthPassword, setReauthPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedback.trim()) {
      setError('Please provide some feedback to refine the prompt.');
      return;
    }

    const storageKey = `${selectedModel}_api_key_encrypted`;
    const passwordCookieName = `api_key_password_${selectedModel}`;

    const encryptedApiKey = localStorage.getItem(storageKey);
    const password = getCookie(passwordCookieName);

    if (encryptedApiKey && !password) {
      setIsReauthenticating(true);
      return;
    }

    setIsLoading(true);
    setError('');

    const payload = {
      original_prompt: originalPrompt,
      final_prompt: finalPrompt,
      user_feedback: feedback,
      api_key: encryptedApiKey,
      password: password,
      style: style,
      framework: framework,
      selected_model: selectedModel,
      selected_groq_model: selectedGroqModel,
    };

    try {
      const response = await fetch('https://promptnova.onrender.com/update_prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to refine prompt.');
      }

      const data = await response.json();
      onRefined(data.updated_prompt);
      onClose();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'An unknown error occurred.');
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

    const storageKey = `${selectedModel}_api_key_encrypted`;
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
        await handleSubmit(e);

    } catch {
        setError("Decryption failed. Incorrect password.");
        setIsLoading(false);
    }
  };

  if (isReauthenticating) {
    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" onClick={onClose}>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl p-6 max-w-xl w-full" onClick={e => e.stopPropagation()}>
                <h2 className="text-2xl font-bold mb-2 text-gray-800 dark:text-gray-100">Session Expired</h2>
                <p className="text-gray-600 dark:text-gray-400 mb-4 text-sm">Please re-enter your password to continue.</p>
                <form onSubmit={handleReauthSubmit}>
                    <div className="mb-4">
                        <label htmlFor="reauth-password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Password</label>
                        <div className="relative">
                            <input id="reauth-password" type={showPassword ? 'text' : 'password'} value={reauthPassword} onChange={(e) => setReauthPassword(e.target.value)} className="w-full p-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500" placeholder="Enter password" autoFocus />
                            <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200">
                                {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                            </button>
                        </div>
                    </div>
                    {error && <p className="text-red-500 dark:text-red-400 text-sm mb-4">{error}</p>}
                    <div className="flex justify-end gap-4">
                        <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-100 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">Cancel</button>
                        <button type="submit" disabled={isLoading} className="px-4 py-2 bg-gray-800 dark:bg-blue-600 text-white rounded-md flex items-center gap-2 disabled:bg-gray-400 dark:disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors">
                            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                            {isLoading ? 'Verifying...' : 'Confirm & Refine'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl p-6 max-w-xl w-full" onClick={e => e.stopPropagation()}>
        <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">Refine Your Prompt</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="feedback" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              What didn’t you like? What could be improved?
            </label>
            <textarea
              id="feedback"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              className="w-full p-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 min-h-[100px]"
              placeholder="e.g., 'The response was too generic. Make it sound more like a pirate.'"
            />
          </div>
          {error && <p className="text-red-500 dark:text-red-400 text-sm mb-4">{error}</p>}
          <div className="flex justify-end gap-4">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-100 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">Cancel</button>
            <button type="submit" disabled={isLoading} className="px-4 py-2 bg-gray-800 dark:bg-blue-600 text-white rounded-md flex items-center gap-2 disabled:bg-gray-400 dark:disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors">
              <RefreshCw className={`h-4 w-4 ${isLoading ? 'Refining...' : ''}`} />
              {isLoading ? 'Refining...' : 'Refine'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};