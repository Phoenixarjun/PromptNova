'use client';

import React, { useState, useEffect } from 'react';
import { Loader2, AlertTriangle, Copy, Check, RefreshCw } from 'lucide-react';
import { MarkdownRenderer } from './MarkdownRenderer';

interface ResultDisplayProps {
  result: string;
  isLoading: boolean;
  error: string;
}

interface ParsedResult {
  explanation: string;
  refined_prompt: string;
  // Project-specific fields
  ideas?: string;
  plan?: string;
  architecture?: string;
  isProject?: boolean;
  evaluation?: string;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, isLoading, error }) => {
  const [parsedResult, setParsedResult] = useState<ParsedResult | null>(null);
  const [isCopied, setIsCopied] = useState(false);

  useEffect(() => {
    if (result) {
      try {
        const parsed = JSON.parse(result);
        console.log(parsed);
        // Check for project-specific fields to determine the result type
        if (parsed.ideas || parsed.plan || parsed.architecture || parsed.json_prompt) {
          setParsedResult({
            isProject: true,
            ideas: parsed.ideas || '',
            plan: parsed.plan || '',
            architecture: parsed.architecture || '',
            refined_prompt: parsed.json_prompt ? JSON.stringify(parsed.json_prompt, null, 2) : '',
            explanation: '', // Not applicable for projects in this structure
            evaluation: parsed.evaluation ? JSON.stringify(parsed.evaluation, null, 2) : '',
          });
        } else if (typeof parsed === 'object' && parsed !== null && (parsed.refined_prompt || parsed.explanation)) {
          // Handle standard refine response
          setParsedResult({
            refined_prompt: parsed.refined_prompt || '',
            explanation: parsed.explanation || '',
            isProject: false,
          });
        }
      } catch {
        // Fallback for when result is a non-JSON string that fails to parse
        setParsedResult({ refined_prompt: result, explanation: '', isProject: false });
      }
    } else {
      setParsedResult(null);
    }
  }, [result]);

  const handleCopy = () => {
    if (!parsedResult?.refined_prompt) return;
    navigator.clipboard.writeText(parsedResult.refined_prompt);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleRefine = () => {
    window.dispatchEvent(new CustomEvent('show-refine-modal'));
  };

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
      <div className="my-8 p-8 bg-red-50 dark:bg-red-950/20 rounded-lg shadow-md max-w-3xl mx-auto border border-red-200 dark:border-red-500/30 flex items-center">
        <AlertTriangle className="h-8 w-8 text-red-500 dark:text-red-400" />
        <div className="ml-4">
          <p className="font-semibold text-red-700 dark:text-red-300">An error occurred:</p>
          <p className="text-red-600 dark:text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  if (!parsedResult) {
    return null;
  }

  return (
    <div className="max-w-3xl mx-auto my-8 space-y-8">
      {/* Project Mode Display */}
      {parsedResult.isProject ? (
        <>
          <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-extrabold text-gray-800 dark:text-gray-100">Project Generation Result</h2>
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
          <div className="space-y-6 overflow-hidden">
            {parsedResult.architecture && (
              <div>
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Architecture</h3>
                <div className="bg-white dark:bg-gray-900 p-6 border border-gray-200 dark:border-gray-700 rounded-md">
                  <MarkdownRenderer content={parsedResult.architecture} />
                </div>
              </div>
            )}
            {parsedResult.refined_prompt && (
              <div>
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">JSON Prompt</h3>
                <div className="bg-white dark:bg-gray-900 p-6 border border-gray-200 dark:border-gray-700 rounded-md">
                  <MarkdownRenderer content={`\`\`\`json\n${parsedResult.refined_prompt}\n\`\`\``} />
                </div>
              </div>
            )}
          </div>
        </>
      ) : (
        <>
          {parsedResult.refined_prompt && (
            <div className="space-y-6">
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
                <MarkdownRenderer content={parsedResult.refined_prompt} />
              </div>
              {parsedResult.explanation && (
                <div className="mt-6">
                  <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-4">Explanation</h3>
                  <div className="bg-white dark:bg-gray-900 p-6 border border-gray-200 dark:border-gray-700 rounded-md">
                    <MarkdownRenderer content={parsedResult.explanation} />
                  </div>
                </div>
              )}
              </div>
          )}
        </>
      )}
    </div>
  );
};
