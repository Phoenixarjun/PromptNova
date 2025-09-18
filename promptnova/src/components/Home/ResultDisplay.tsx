"use client";

import React, { useState, useEffect } from 'react';
import { Loader2, AlertTriangle } from 'lucide-react';
import { MarkdownRenderer } from './MarkdownRenderer';

interface ResultDisplayProps {
  result: string;
  isLoading: boolean;
  error: string;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, isLoading, error }) => {
  const [parsedPrompt, setParsedPrompt] = useState('');
  const [parsedExplanation, setParsedExplanation] = useState('');

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
      
      const cleanedPrompt = promptPart.replace(/^```[\w\s]*\n?|```$/g, "").trim();
      
      setParsedPrompt(cleanedPrompt);
      setParsedExplanation(explanationPart.trim());
    } else {
      setParsedPrompt('');
      setParsedExplanation('');
    }
  }, [result]);

  if (isLoading) {
    return (
      <div className="mt-8 p-8 bg-gray-50 rounded-lg shadow-md max-w-3xl mx-auto border border-gray-200 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-gray-500" />
        <p className="ml-4 text-gray-600">Generating refined prompt...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-8 p-8 bg-red-50 rounded-lg shadow-md max-w-3xl mx-auto border border-red-200 flex items-center">
        <AlertTriangle className="h-8 w-8 text-red-500" />
        <div className="ml-4">
          <p className="font-semibold text-red-700">An error occurred:</p>
          <p className="text-red-600">{error}</p>
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
        <div className="mt-8 pt-6 border-t border-gray-200 space-y-6">
          <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-800">Generated Prompt</h2>
          </div>
          <div className="bg-white p-6 border border-gray-200 rounded-md"><MarkdownRenderer content={parsedPrompt} /></div>
          {parsedExplanation && (
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-gray-800">Explanation</h3>
              <div className="bg-white p-6 border border-gray-200 rounded-md">
                <MarkdownRenderer content={parsedExplanation} />
              </div>
            </div>
          )}
        </div>)}
    </div>
  );
};