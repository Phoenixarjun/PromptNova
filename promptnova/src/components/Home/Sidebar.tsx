"use client";

import React, { useState, useEffect, useCallback } from 'react';
import CryptoJS from 'crypto-js';
import { Settings, Eye, EyeOff, Info } from 'lucide-react';
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

interface SidebarProps {
    selectedModel: string;
    setSelectedModel: (model: string) => void;
    selectedGroqModel: string;
    setSelectedGroqModel: (model: string) => void;
}

const getStorageKey = (model: string) => `${model}_api_key_encrypted`;

const MODELS_CONFIG: { [key: string]: { label: string; url: string; models?: { label: string; value: string }[] } } = {
    gemini: {
        label: "Gemini API Key",
        url: "https://aistudio.google.com/app/apikey",
    },
    mistral: {
        label: "Mistral API Key",
        url: "https://console.mistral.ai/api-keys/",
    },
    groq: {
        label: "Groq API Key",
        url: "https://console.groq.com/keys",
        models: [
            { label: "Default (Llama3 8b)", value: "llama3-8b-8192" },
            { label: "Qwen3 32b", value: "qwen/qwen3-32b" },
            { label: "Llama 3.1 8b Instant", value: "llama-3.1-8b-instant" },
            { label: "Compound", value: "groq/compound" },
            { label: "Compound Mini", value: "groq/compound-mini" },
            { label: "GPT-OSS 120b", value: "openai/gpt-oss-120b" },
            { label: "GPT-OSS 20b", value: "openai/gpt-oss-20b" },
            { label: "Llama 3.3 70b Versatile", value: "llama-3.3-70b-versatile" },
            { label: "Llama 4 Scout 17b", value: "meta-llama/llama-4-scout-17b-16e-instruct" },
        ]
    }
};

export const Sidebar: React.FC<SidebarProps> = ({ selectedModel, setSelectedModel, selectedGroqModel, setSelectedGroqModel }) => {
    const [apiKeyInput, setApiKeyInput] = useState('');
    const [isKeySaved, setIsKeySaved] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    
    const [isPrompting, setIsPrompting] = useState(false);
    const [password, setPassword] = useState('');
    const [promptConfig, setPromptConfig] = useState({ title: '', action: '' });
    const [promptError, setPromptError] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [verifiedPassword, setVerifiedPassword] = useState<string | null>(null);

    const resetPrompt = useCallback(() => {
        setIsPrompting(false);
        setPassword('');
        setPromptError('');
        setShowPassword(false);
        setPromptConfig({ title: '', action: '' });
    }, []);

    useEffect(() => {
        const storageKey = getStorageKey(selectedModel);
        const storedKey = localStorage.getItem(storageKey);
        if (storedKey) {
            setIsKeySaved(true);
            setApiKeyInput('********************');
            setIsEditing(false);
        } else {
            setIsKeySaved(false);
            setApiKeyInput('');
            setIsEditing(true);
        }
    }, [selectedModel]);

    const performSaveNewKey = (pwd: string) => {
        const storageKey = getStorageKey(selectedModel);
        const encrypted = CryptoJS.AES.encrypt(apiKeyInput, pwd).toString();
        localStorage.setItem(storageKey, encrypted);
        document.cookie = `api_key_password_${selectedModel}=${pwd};max-age=${7 * 24 * 60 * 60};path=/;SameSite=Lax`;

        setIsKeySaved(true);
        setIsEditing(false);
        setApiKeyInput('********************');
        resetPrompt();
    };

    const performEdit = (pwd: string) => {
        const storageKey = getStorageKey(selectedModel);
        const encryptedKey = localStorage.getItem(storageKey);

        if (!encryptedKey) {
            setPromptError("Encrypted key not found. Please save it again.");
            return;
        }

        try {
            const decryptedBytes = CryptoJS.AES.decrypt(encryptedKey, pwd);
            const decryptedKey = decryptedBytes.toString(CryptoJS.enc.Utf8);

            if (!decryptedKey) {
                setPromptError('Incorrect password.');
                return;
            }

            setApiKeyInput(decryptedKey);
            setIsEditing(true);
            setVerifiedPassword(pwd);
            document.cookie = `api_key_password_${selectedModel}=${pwd};max-age=${7 * 24 * 60 * 60};path=/;SameSite=Lax`;
            resetPrompt();
        } catch (e) {
            console.error("Decryption failed:", e);
            setPromptError("Decryption failed. The key might be corrupted or password is wrong.");
        }
    };

    const performDelete = (pwd: string) => {
        const storageKey = getStorageKey(selectedModel);
        const encryptedKey = localStorage.getItem(storageKey);
        if (!encryptedKey) {
            setPromptError("Key not found.");
            return;
        }

        try {
            const decryptedBytes = CryptoJS.AES.decrypt(encryptedKey, pwd);
            const decryptedKey = decryptedBytes.toString(CryptoJS.enc.Utf8);

            if (!decryptedKey) {
                setPromptError('Incorrect password.');
                return;
            }

            localStorage.removeItem(storageKey);
            document.cookie = `api_key_password_${selectedModel}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
            setIsKeySaved(false);
            setApiKeyInput('');
            setIsEditing(true);
            resetPrompt();
        } catch (e) {
            console.error("Deletion failed:", e);
            setPromptError("Decryption failed. The key might be corrupted or password is wrong.");
        }
    };

    const handlePasswordSubmit = () => {
        if (!password) {
            setPromptError('Password cannot be empty.');
            return;
        }
        setPromptError('');

        switch (promptConfig.action) {
            case 'save_new':
                performSaveNewKey(password);
                break;
            case 'edit':
                performEdit(password);
                break;
            case 'delete':
                performDelete(password);
                break;
        }
    };

    const handleSaveClick = () => {
        if (!apiKeyInput || apiKeyInput === '********************') return;

        if (isKeySaved && isEditing && verifiedPassword) {
            const storageKey = getStorageKey(selectedModel);
            const encrypted = CryptoJS.AES.encrypt(apiKeyInput, verifiedPassword).toString();
            localStorage.setItem(storageKey, encrypted);
            document.cookie = `api_key_password_${selectedModel}=${verifiedPassword};max-age=${7 * 24 * 60 * 60};path=/;SameSite=Lax`;

            setIsEditing(false);
            setVerifiedPassword(null);
            setApiKeyInput('********************');
        } else if (!isKeySaved) {
            setPromptConfig({ title: 'Set a Password to Secure Your Key', action: 'save_new' });
            setIsPrompting(true);
        }
    };

    const handleEditClick = () => {
        setPromptConfig({ title: 'Enter Password to Edit Key', action: 'edit' });
        setIsPrompting(true);
    };

    const handleDeleteClick = () => {
        setPromptConfig({ title: 'Enter Password to Delete Key', action: 'delete' });
        setIsPrompting(true);
    };

    const handleCancelEdit = () => {
        setIsEditing(false);
        setVerifiedPassword(null);
        setApiKeyInput('********************');
    };

    const PasswordPrompt = () => (
        <div className="mt-4 p-4 bg-gray-200 dark:bg-gray-800 rounded-md border border-gray-300 dark:border-gray-700">
            <h3 className="text-sm font-semibold mb-2 text-gray-800 dark:text-gray-200">{promptConfig.title}</h3>
            <div className="relative">
                <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handlePasswordSubmit()}
                    className="w-full p-2 pr-10 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-200 rounded-md text-sm"
                    placeholder="Enter password"
                    autoFocus
                />
                <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
            </div>
            {promptError && <p className="text-red-600 text-xs mt-1">{promptError}</p>}
            <div className="flex space-x-2 mt-2">
                <button onClick={handlePasswordSubmit} className="flex-1 bg-gray-800 dark:bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 dark:hover:bg-blue-700 text-sm font-medium">
                    Confirm
                </button>
                <button onClick={resetPrompt} className="flex-1 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 px-4 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 text-sm font-medium">
                    Cancel
                </button>
            </div>
        </div>
    );

    const renderButtons = () => {
        if (isPrompting) {
            return <PasswordPrompt />;
        }

        if (isEditing) {
            if (isKeySaved) { // Editing an existing key
                return (
                    <div className="flex space-x-2">
                        <button onClick={handleSaveClick} className="flex-1 bg-gray-800 dark:bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 dark:hover:bg-blue-700 text-sm font-semibold transition-colors">
                            Save
                        </button>
                        <button onClick={handleCancelEdit} className="flex-1 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 px-4 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 text-sm font-medium">
                            Cancel
                        </button>
                    </div>
                );
            } else { // Entering a new key
                return (
                    <button onClick={handleSaveClick} className="w-full bg-gray-800 dark:bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 dark:hover:bg-blue-700 text-sm font-semibold transition-colors disabled:bg-gray-400 dark:disabled:bg-gray-500" disabled={!apiKeyInput}>
                        Save Key
                    </button>
                );
            }
        }

        if (isKeySaved) { // Key is saved and locked
            return (
                <div className="flex space-x-2">
                    <button onClick={handleEditClick} className="flex-1 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 px-4 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 text-sm font-medium transition-colors">
                        Edit
                    </button>
                    <button onClick={handleDeleteClick} className="flex-1 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 text-sm font-medium transition-colors">
                        Delete
                    </button>
                </div>
            );
        }

        return null;
    };

    return (
        <aside className="w-full md:w-64 lg:w-72 flex-shrink-0 bg-gray-100 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 p-6">
            <div className="space-y-4 sticky top-24">
                <div className="flex items-center gap-2">
                    <Settings className="h-5 w-5 text-gray-600" />
                    <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Settings</h2>
                </div>

                <div>
                    <div className="flex items-center justify-between mb-2">
                        <Label htmlFor="model-select" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            Choose Model
                        </Label>
                        <Popover>
                            <PopoverTrigger asChild>
                                <Button variant="ghost" size="icon" className="h-6 w-6">
                                    <Info className="h-4 w-4" />
                                    <span className="sr-only">Model Information</span>
                                </Button>
                            </PopoverTrigger>
                            <PopoverContent className="w-80" side="top">
                                <div className="flex flex-col space-y-2 text-sm">
                                    <h4 className="font-semibold">Model Recommendations</h4>
                                    <p>
                                        <span className="font-bold">Gemini:</span> Expert model that provides very detailed, long, and well-structured prompts. It may take a bit more time but is highly recommended for quality.
                                    </p>
                                    <p>
                                        <span className="font-bold">Groq:</span> Faster than Gemini, but due to context window limitations, it provides smaller, more concise prompts. Still a great choice for quick iterations.
                                    </p>
                                    <p>
                                        <span className="font-bold">Mistral:</span> A middle ground in terms of performance, providing average-length prompts with good quality.
                                    </p>
                                </div>
                            </PopoverContent>
                        </Popover>
                    </div>
                    <Select value={selectedModel} onValueChange={setSelectedModel}>
                        <SelectTrigger id="model-select" className="w-full mt-2">
                            <SelectValue placeholder="Select a model" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="gemini">Gemini</SelectItem>
                            <SelectItem value="mistral">Mistral</SelectItem>
                            <SelectItem value="groq">Groq</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                {selectedModel === 'groq' && (
                    <div>
                        <Label htmlFor="groq-model-select" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            Groq Model
                        </Label>
                        <Select value={selectedGroqModel} onValueChange={setSelectedGroqModel}>
                            <SelectTrigger id="groq-model-select" className="w-full mt-2">
                                <SelectValue placeholder="Select a Groq model" />
                            </SelectTrigger>
                            <SelectContent>
                                {MODELS_CONFIG.groq.models?.map(model => (
                                    <SelectItem key={model.value} value={model.value}>{model.label}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                )}

                <div>
                    <div className="flex items-center justify-between mb-2">
                        <Label htmlFor="api-key-input" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            {MODELS_CONFIG[selectedModel].label}
                        </Label>
                        <Popover>
                            <PopoverTrigger asChild>
                                <Button variant="ghost" size="icon" className="h-6 w-6">
                                    <Info className="h-4 w-4" />
                                    <span className="sr-only">API Key Instructions</span>
                                </Button>
                            </PopoverTrigger>
                            <PopoverContent className="w-80" side="top">
                                <div className="flex flex-col space-y-2 text-sm">
                                    <h4 className="font-semibold">How to get your {MODELS_CONFIG[selectedModel].label}</h4>
                                    <p>
                                        Go to{" "}
                                        <a
                                            href={MODELS_CONFIG[selectedModel].url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-blue-500 hover:underline"
                                        >
                                            the official website
                                        </a>, create an account, and generate your API key.
                                    </p>
                                </div>
                            </PopoverContent>
                        </Popover>
                    </div>
                    <div className="relative">
                        <Input
                            id="api-key-input"
                            type={isEditing ? 'text' : 'password'}
                            className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-sm"
                            value={apiKeyInput}
                            onChange={(e) => setApiKeyInput(e.target.value)}
                            placeholder="Enter your API key"
                            readOnly={!isEditing}
                        />
                    </div>
                </div>

                {renderButtons()}

                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                    Your API key is stored securely in your browser's local storage and is never sent to our servers.
                </p>
            </div>
        </aside>
    );
};
