'use client';

import React, { useState } from 'react';
import { Loader2, AlertTriangle, Copy, Check, Info } from 'lucide-react';
import { MarkdownRenderer } from '../Home/MarkdownRenderer';

export interface Evaluation {
  success: boolean;
  reason?: string;
  final_polish_needed?: string;
}

export interface ProjectManiaMetadata {
  refinement_history?: { evaluation: Evaluation }[];
  template_type?: 'general' | 'crewai' | 'autogen';
}

interface ProjectManiaResultDisplayProps {
  result: string;
  metadata?: ProjectManiaMetadata;
  isLoading: boolean;
  error: string;
  templateType: 'general' | 'crewai' | 'autogen';
}

export const ProjectManiaResultDisplay: React.FC<ProjectManiaResultDisplayProps> = ({ result, metadata, isLoading, error, templateType }) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = () => {
    if (!result) return;
    navigator.clipboard.writeText(result);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  if (isLoading) {
    return (
      <div className="mt-8 p-8 bg-gray-50 dark:bg-gray-800/50 rounded-lg shadow-md max-w-3xl mx-auto border border-gray-200 dark:border-gray-700 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-gray-500 dark:text-gray-400" />
        <p className="ml-4 text-gray-600 dark:text-gray-300">Generating your blueprint...</p>
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

  if (!result) {
    return null;
  }

  // Extract evaluation from metadata if available
  const refinementHistory = metadata?.refinement_history || [];
  const lastIteration = refinementHistory.length > 0 ? refinementHistory[refinementHistory.length - 1] : null;
  const evaluation = lastIteration?.evaluation;

  // Conditional wrapping: Wrap in python block for crewai/autogen, otherwise raw result
  const effectiveTemplateType = metadata?.template_type || templateType;
  const contentToRender = (effectiveTemplateType === 'crewai' || effectiveTemplateType === 'autogen') 
    ? `\`\`\`python\n${result}\n\`\`\`` 
    : result;

  return (
    <div className="max-w-4xl mx-auto my-8 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      {/* Main Template Result */}
      <div>
        <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-extrabold text-gray-800 dark:text-gray-100 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
            Generated Blueprint
            </h2>
            <div className="flex items-center gap-2">
                <button 
                onClick={handleCopy} 
                className="inline-flex items-center gap-1.5 rounded-md bg-gray-100 dark:bg-gray-700 px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                >
                {isCopied ? <Check className="h-4 w-4 text-green-600" /> : <Copy className="h-4 w-4" />}
                {isCopied ? 'Copied' : 'Copy'}
                </button>
            </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm">
            <MarkdownRenderer content={contentToRender} />
        </div>
      </div>

      {/* Evaluation Report */}
      {evaluation && (
        <div className="mt-8">
            <div className="flex items-center gap-2 mb-4">
                <Info className="h-6 w-6 text-blue-500" />
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">Evaluation Report</h3>
            </div>
            
            <div className="bg-white dark:bg-gray-900 p-6 border border-gray-200 dark:border-gray-700 rounded-md">
                <div className="grid gap-4">
                    <div>
                        <span className="font-semibold text-gray-700 dark:text-gray-300">Status: </span>
                        <span className={`font-bold ${evaluation.success ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                            {evaluation.success ? 'Passed' : 'Needs Improvement'}
                        </span>
                    </div>
                    
                    {evaluation.reason && (
                        <div>
                            <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-1">Analysis:</h4>
                            <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                                {evaluation.reason}
                            </p>
                        </div>
                    )}

                    {evaluation.final_polish_needed && (
                        <div>
                            <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-1">Suggestions:</h4>
                            <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                                {evaluation.final_polish_needed}
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
      )}

    </div>
  );
};
