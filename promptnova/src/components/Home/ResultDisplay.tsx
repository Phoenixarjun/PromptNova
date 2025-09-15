"use client";

import React, { useState } from 'react';
import { Loader2, AlertTriangle, Clipboard, Check } from 'lucide-react';

interface ResultDisplayProps {
  result: string;
  isLoading: boolean;
  error: string;
}

export const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, isLoading, error }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(result).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

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
    <div className="mt-8 p-8 bg-white rounded-lg shadow-lg max-w-3xl mx-auto border border-gray-200 relative group">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Refined Prompt</h2>
      <pre className="bg-gray-100 p-4 rounded-md text-gray-800 whitespace-pre-wrap font-mono text-sm">
        <code>{result}</code>
      </pre>
      <button
        onClick={handleCopy}
        className="absolute top-8 right-8 p-2 bg-gray-200 text-gray-600 rounded-md transition-colors duration-200 hover:bg-gray-300"
        aria-label="Copy prompt"
      >
        {copied ? <Check className="h-5 w-5 text-green-600" /> : <Clipboard className="h-5 w-5" />}
      </button>
    </div>
  );
};