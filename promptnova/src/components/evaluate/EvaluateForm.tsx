"use client";

import React from 'react';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';
import { FormField } from './FormField';

interface EvaluateFormProps {
  promptToEvaluate: string;
  setPromptToEvaluate: (value: string) => void;
  initialPrompt: string;
  setInitialPrompt: (value: string) => void;
  handleSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
}

export const EvaluateForm: React.FC<EvaluateFormProps> = ({
  promptToEvaluate,
  setPromptToEvaluate,
  initialPrompt,
  setInitialPrompt,
  handleSubmit,
  isLoading,
}) => {
  return (
    <div className="p-8 bg-gray-50 dark:bg-gray-900/50 rounded-lg shadow-md max-w-3xl mx-auto my-8 border border-gray-200 dark:border-gray-800">
      <form onSubmit={handleSubmit} className="space-y-6">
        <FormField
          id="prompt_to_evaluate"
          label="Prompt to Evaluate"
          value={promptToEvaluate}
          onChange={(e) => setPromptToEvaluate(e.target.value)}
          placeholder="Enter the prompt you want to score..."
          required
        />
        <FormField
          id="initial_prompt"
          label="Initial Prompt (Optional)"
          value={initialPrompt}
          onChange={(e) => setInitialPrompt(e.target.value)}
          placeholder="If the prompt above is a refined version, provide the original one here for a comparative score."
          helperText="Providing the initial prompt helps the T-RAG framework evaluate goal alignment more accurately."
          minHeight="min-h-[100px]"
        />
        <Button type="submit" disabled={isLoading} className="w-full bg-gray-800 text-white dark:bg-gray-300 dark:text-gray-800 px-6 py-3 rounded-md hover:bg-gray-700 dark:hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 font-semibold text-lg disabled:bg-gray-400 dark:disabled:bg-gray-500 disabled:cursor-not-allowed sm:w-auto">
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Evaluating...
            </>
          ) : (
            'Get Score'
          )}
        </Button>
      </form>
    </div>
  );
};