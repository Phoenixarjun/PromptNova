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

const API_KEY_STORAGE_ITEM = 'gemini_api_key_encrypted';

export const Sidebar = () => {
    const [apiKeyInput, setApiKeyInput] = useState('');
    const [isKeySaved, setIsKeySaved] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    
    // State for the password prompt
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
        const storedKey = localStorage.getItem(API_KEY_STORAGE_ITEM);
        if (storedKey) {
            setIsKeySaved(true);
            setApiKeyInput('********************');
        } else {
            setIsEditing(true); 
        }
    }, []);

    const performSaveNewKey = (pwd: string) => {
        // Encrypt the key. CryptoJS handles salting automatically.
        const encrypted = CryptoJS.AES.encrypt(apiKeyInput, pwd).toString();
        localStorage.setItem(API_KEY_STORAGE_ITEM, encrypted);
        // Save password to a cookie that expires in 7 days
        document.cookie = `api_key_password=${pwd};max-age=${7 * 24 * 60 * 60};path=/;SameSite=Lax`;
        
        setIsKeySaved(true);
        setIsEditing(false);
        setApiKeyInput('********************');
        resetPrompt();
    };

    const performEdit = (pwd: string) => {
        const encryptedKey = localStorage.getItem(API_KEY_STORAGE_ITEM);

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
            setVerifiedPassword(pwd); // Store password for the save action
            // Refresh the password cookie for another 7 days
            document.cookie = `api_key_password=${pwd};max-age=${7 * 24 * 60 * 60};path=/;SameSite=Lax`;
            resetPrompt();
        } catch (e) {
            console.error("Decryption failed:", e);
            setPromptError("Decryption failed. The key might be corrupted or password is wrong.");
        }
    };

    const performDelete = (pwd: string) => {
        const encryptedKey = localStorage.getItem(API_KEY_STORAGE_ITEM);
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

            localStorage.removeItem(API_KEY_STORAGE_ITEM);
            document.cookie = 'api_key_password=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
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
            // This is an update after editing. We have the verified password.
            const encrypted = CryptoJS.AES.encrypt(apiKeyInput, verifiedPassword).toString();
            localStorage.setItem(API_KEY_STORAGE_ITEM, encrypted);
            // Refresh the password cookie for another 7 days
            document.cookie = `api_key_password=${verifiedPassword};max-age=${7 * 24 * 60 * 60};path=/;SameSite=Lax`;
            
            setIsEditing(false);
            setVerifiedPassword(null);
            setApiKeyInput('********************');
        } else if (!isKeySaved) {
            // This is a brand new key.
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
                        <Label htmlFor="api-key-input" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            Gemini API Key
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
                                    <h4 className="font-semibold">How to get your Gemini API Key</h4>
                                    <ol className="list-decimal list-inside space-y-1">
                                        <li>
                                            Go to{" "}
                                            <a
                                                href="https://aistudio.google.com/app/apikey"
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-blue-500 hover:underline"
                                            >
                                                Google AI Studio
                                            </a>
                                            .
                                        </li>
                                        <li>
                                            Click on <strong>"Get API key"</strong>.
                                        </li>
                                        <li>
                                            Click on <strong>"Create API key in new project"</strong>.
                                        </li>
                                        <li>Copy the generated API key and paste it here.</li>
                                    </ol>
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
