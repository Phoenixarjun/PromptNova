'use client'
import React, { useState } from 'react';
import { Sparkles, Plus, X, Loader2, Eye, EyeOff, RefreshCw } from 'lucide-react';
import { generateProjectManiaTemplate, ProjectManiaRequest } from './projectManiaApi';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Label } from '../ui/label';
import { FormField } from '../evaluate/FormField';
import CryptoJS from 'crypto-js';

import { ProjectManiaMetadata } from './ProjectManiaResultDisplay';

interface ProjectManiaFormProps {
  setResult: (result: string) => void;
  setMetadata: (metadata: ProjectManiaMetadata | null) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string) => void;
  isLoading: boolean;
  selectedModel: string;
  selectedGroqModel: string;
  templateType: 'general' | 'crewai' | 'autogen';
  setTemplateType: (type: 'general' | 'crewai' | 'autogen') => void;
}

export const ProjectManiaForm: React.FC<ProjectManiaFormProps> = ({
  setResult,
  setMetadata,
  setIsLoading,
  setError,
  isLoading,
  selectedModel,
  selectedGroqModel,
  templateType,
  setTemplateType
}) => {
  const [intent, setIntent] = useState('');
  const [variables, setVariables] = useState<string[]>([]);
  const [newVariable, setNewVariable] = useState('');
  // templateType state removed (lifted up)
  const [promptLength, setPromptLength] = useState<'low' | 'medium' | 'high'>('medium');

  // Auth state
  const [isReauthenticating, setIsReauthenticating] = useState(false);
  const [reauthPassword, setReauthPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const getCookie = (name: string): string | null => {
    if (typeof document === 'undefined') return null;
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
  };

  const getStorageKey = (model: string) => `${model}_api_key_encrypted`;

  const handleAddVariable = () => {
    if (newVariable.trim()) {
      setVariables([...variables, newVariable.trim()]);
      setNewVariable('');
    }
  };

  const handleRemoveVariable = (index: number) => {
    setVariables(variables.filter((_, i) => i !== index));
  };

  const handleReauthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reauthPassword) {
        setError('Password cannot be empty.');
        return;
    }
    // Don't set global loading here to keep the modal interactive, or handle carefully
    // But we can set a local loading state if we wanted. For now, we just verify.
    
    const storageKey = getStorageKey(selectedModel);
    const encryptedKey = localStorage.getItem(storageKey);
    if (!encryptedKey) {
        setError("Encrypted key not found. Please save it again in Settings.");
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
        setError('');
        
        // Retry submission automatically
        await submitForm(reauthPassword);

    } catch {
        setError("Decryption failed. Incorrect password.");
    }
  };

  const submitForm = async (passwordOverride?: string) => {
    setIsLoading(true);
    setError('');
    setResult('');
    setMetadata(null);

    const storageKey = getStorageKey(selectedModel);
    const passwordCookieName = `api_key_password_${selectedModel}`;
    const encryptedApiKey = localStorage.getItem(storageKey);
    const password = passwordOverride || getCookie(passwordCookieName);

    const payload: ProjectManiaRequest = {
      intent,
      variables,
      template_type: templateType,
      api_key: encryptedApiKey,
      password: password,
      selected_model: selectedModel,
      selected_groq_model: selectedGroqModel,
      prompt_length: promptLength
    };

    try {
      const response = await generateProjectManiaTemplate(payload);
      console.log(response);
      setResult(response.final_template);
      setMetadata(response.metadata);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!intent.trim()) {
      setError('Please enter your intent.');
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

    await submitForm(password || undefined);
  };

  return (
    <>
      {isReauthenticating && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4" onClick={() => setIsReauthenticating(false)}>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl p-6 max-w-xl w-full" onClick={e => e.stopPropagation()}>
                <h2 className="text-2xl font-bold mb-2 text-gray-800 dark:text-gray-100">Session Expired</h2>
                <p className="text-gray-600 dark:text-gray-400 mb-4 text-sm">Please re-enter your password to continue.</p>
                <form onSubmit={handleReauthSubmit}>
                    <div className="mb-4">
                        <label htmlFor="reauth-password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Password</label>
                        <div className="relative">
                            <input 
                              id="reauth-password" 
                              type={showPassword ? 'text' : 'password'} 
                              value={reauthPassword} 
                              onChange={(e) => setReauthPassword(e.target.value)} 
                              className="w-full p-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500" 
                              placeholder="Enter password" 
                              autoFocus 
                            />
                            <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200">
                                {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />} 
                            </button>
                        </div>
                    </div>
                    <div className="flex justify-end gap-4">
                        <button type="button" onClick={() => setIsReauthenticating(false)} className="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-100 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors">Cancel</button>
                        <button type="submit" className="px-4 py-2 bg-gray-800 dark:bg-blue-600 text-white rounded-md flex items-center gap-2 hover:bg-gray-900 dark:hover:bg-blue-700 transition-colors">
                            <RefreshCw className="h-4 w-4" />
                            Confirm & Generate
                        </button>
                    </div>
                </form>
            </div>
        </div>
      )}

      <Card className="w-full max-w-3xl mx-auto shadow-md border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900/50">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            Project Mania 
          </CardTitle>
          <CardDescription className="text-center">
            Generate comprehensive blueprint templates for your AI projects.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            
            <FormField
              id="intent"
              label="Project Intent"
              value={intent}
              onChange={(e) => setIntent(e.target.value)}
              placeholder="e.g., I want to build a multi-agent system for stock market analysis..."
              required
              minHeight="min-h-[100px]"
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label>Template Type</Label>
                <Select 
                  value={templateType} 
                  onValueChange={(val: 'general' | 'crewai' | 'autogen') => setTemplateType(val)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="general">General Prompt Template</SelectItem>
                    <SelectItem value="crewai">CrewAI Configuration</SelectItem>
                    <SelectItem value="autogen">AutoGen Script</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Prompt Length</Label>
                <Select 
                  value={promptLength} 
                  onValueChange={(val: 'low' | 'medium' | 'high') => setPromptLength(val)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select length" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low (Concise)</SelectItem>
                    <SelectItem value="medium">Medium (Balanced)</SelectItem>
                    <SelectItem value="high">High (Detailed)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Variables</Label>
                <div className="flex gap-2">
                  <Input
                    placeholder="e.g., stock_symbol"
                    value={newVariable}
                    onChange={(e) => setNewVariable(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleAddVariable();
                      }
                    }}
                  />
                  <Button type="button" onClick={handleAddVariable} size="icon" variant="outline">
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {variables.map((v, i) => (
                    <span key={i} className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                      {v}
                      <button type="button" onClick={() => handleRemoveVariable(i)} className="hover:text-blue-600 dark:hover:text-blue-400">
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <Button 
              type="submit" 
              className="w-full bg-gray-800 text-white dark:bg-gray-300 dark:text-gray-800 px-6 py-3 rounded-md hover:bg-gray-700 dark:hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 font-semibold text-lg disabled:bg-gray-400 dark:disabled:bg-gray-500 disabled:cursor-not-allowed"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating Blueprint...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" />
                  Generate Template
                </>
              )}
            </Button>

          </form>
        </CardContent>
      </Card>
    </>
  );
};
