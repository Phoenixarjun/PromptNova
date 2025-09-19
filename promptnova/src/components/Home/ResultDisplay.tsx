"use client";

import React, { useState, useEffect } from 'react';
import { Loader2, AlertTriangle, Copy, Check, RefreshCw } from 'lucide-react';
import { MarkdownRenderer } from './MarkdownRenderer';

interface ResultDisplayProps {
  result: string;
  isLoading: boolean;
  error: string;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, isLoading, error }) => {
  const [parsedPrompt, setParsedPrompt] = useState('');
  const [parsedExplanation, setParsedExplanation] = useState('');
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(parsedPrompt);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleRefine = () => {
    // This will be caught by an event listener in the Form component
    window.dispatchEvent(new CustomEvent('show-refine-modal'));
  };

  useEffect(() => {
    if (result) {
      const explanationSeparator = "**Explanation of Improvements and Rationale:**";
      const promptSeparator = "**Refined Prompt:**";
      
      let promptPart = result;
      let explanationPart = '';

      if (result.includes(explanationSeparator)) {
        const parts = result.split(explanationSeparator);
        promptPart = parts[0];
        explanationPart = parts[1] || '';
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
      setParsedExplanation(explanationPart.trim());
    } else {
      setParsedPrompt('');
      setParsedExplanation('');
    }
  }, [result]);

  if (isLoading) {
    return (
      <div className="mt-8 p-8 bg-gray-50 dark:bg-gray-800/50 rounded-lg shadow-md max-w-3xl mx-auto border border-gray-200 dark:border-gray-700 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-gray-500 dark:text-gray-400" />
        <p className="ml-4 text-gray-600 dark:text-gray-300">Generating refined prompt...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-8 p-8 bg-red-50 dark:bg-red-950/20 rounded-lg shadow-md max-w-3xl mx-auto border border-red-200 dark:border-red-500/30 flex items-center">
        <AlertTriangle className="h-8 w-8 text-red-500 dark:text-red-400" />
        <div className="ml-4">
          <p className="font-semibold text-red-700 dark:text-red-300">An error occurred:</p>
          <p className="text-red-600 dark:text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <div className="max-w-3xl mx-auto my-8">
      {result && !isLoading && !error && (
        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700 space-y-6">
          <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-800 dark:text-gray-100">Generated Prompt</h2>
              <div className="flex items-center gap-2">
                <button onClick={handleCopy} className="inline-flex items-center gap-1.5 rounded-md bg-gray-100 dark:bg-gray-700 px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
                  {isCopied ? <Check className="h-4 w-4 text-green-600" /> : <Copy className="h-4 w-4" />}
                  {isCopied ? 'Copied' : 'Copy'}
                </button>
                <button onClick={handleRefine} className="inline-flex items-center gap-1.5 rounded-md bg-blue-600 text-white px-3 py-1.5 text-sm font-medium hover:bg-blue-700 dark:hover:bg-blue-500 transition-colors">
                  <RefreshCw className="h-4 w-4" />
                  Refine
                </button>
              </div>
          </div>
          <div className="bg-white dark:bg-gray-900 p-6 border border-gray-200 dark:border-gray-700 rounded-md">
            <pre className="whitespace-pre-wrap font-sans text-sm text-gray-800 dark:text-gray-200">{parsedPrompt}</pre>
          </div>
          {parsedExplanation && (
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100">Explanation</h3>
              <div className="bg-white dark:bg-gray-900 p-6 border border-gray-200 dark:border-gray-700 rounded-md">
                <MarkdownRenderer content={parsedExplanation} />
              </div>
            </div>
          )}
        </div>)}
    </div>
  );
};