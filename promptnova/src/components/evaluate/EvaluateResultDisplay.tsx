"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Loader2, Sparkles, AlertTriangle, CheckCircle } from 'lucide-react';

interface FullEvaluationResult {
  llm_as_judge: {
    clarity: number;
    specificity: number;
    context: number;
    goal_alignment: number;
    measurability: number;
    overall: number;
    comment: string;
  };
  t_rag: {
    intent_alignment: number;
    completeness: number;
    relevance: number;
    ambiguity: number;
    overall: number;
  };
  mar_framework: {
    clarity: number;
    completeness: number;
    relevance: number;
    structure: number;
    creativity_precision_balance: number;
    overall_score: number;
  };
  final_evaluation: {
    final_score: number;
    strengths: string;
    areas_for_improvement: string;
    report: string;
  };
}

interface EvaluateResultDisplayProps {
  result: FullEvaluationResult | null;
  isLoading: boolean;
  error: string | null;
}

const ScoreGauge = ({ score }: { score: number }) => {
  const getScoreColor = (value: number) => {
    if (value >= 80) return 'text-green-500';
    if (value >= 50) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <div className="relative flex h-32 w-32 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800">
      <div className={`text-4xl font-bold ${getScoreColor(score)}`}>
        {score.toFixed(1)}
      </div>
    </div>
  );
};

export const EvaluateResultDisplay: React.FC<EvaluateResultDisplayProps> = ({ result, isLoading, error }) => {
  if (isLoading) {
    return null; // The loading indicator is in the form button
  }

  if (error) {
    return (
      <div className="mt-6 rounded-md border border-red-300 bg-red-50 p-4 text-red-700">
        <div className="flex items-center">
          <AlertTriangle className="mr-2 h-5 w-5" />
          <p><strong>Error:</strong> {error}</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <div className="mt-10">
      <h2 className="mb-6 text-3xl font-bold text-gray-900 dark:text-gray-100">Evaluation Result</h2>
      <Card className="overflow-hidden shadow-lg bg-white dark:bg-gray-900">
        <CardHeader className="bg-gray-50 dark:bg-gray-800/30 p-6">
          <div className="flex flex-col items-center gap-4 text-center sm:flex-row sm:text-left">
            <ScoreGauge score={result.final_evaluation.final_score} />
            <div>
              <CardTitle className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                Final Score: {result.final_evaluation.final_score.toFixed(1)} / 100
              </CardTitle>
              <CardDescription className="mt-1 text-lg text-gray-600 dark:text-gray-400">
                A comprehensive quality rating for your prompt.
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6 p-6">
          <div>
            <h3 className="mb-2 flex items-center text-xl font-semibold text-gray-800 dark:text-gray-100"><CheckCircle className="mr-2 h-5 w-5 text-green-500" />Strengths</h3>
            <p className="text-gray-700 dark:text-gray-300">{result.final_evaluation.strengths}</p>
          </div>
          <div>
            <h3 className="mb-2 flex items-center text-xl font-semibold text-gray-800 dark:text-gray-100"><Sparkles className="mr-2 h-5 w-5 text-blue-500" />Areas for Improvement</h3>
            <p className="text-gray-700 dark:text-gray-300">{result.final_evaluation.areas_for_improvement}</p>
          </div>
          <div>
            <h3 className="mb-3 text-xl font-semibold text-gray-800 dark:text-gray-100">Detailed Report</h3>
            <div className="whitespace-pre-wrap rounded-md bg-gray-100 dark:bg-gray-800/50 p-4 font-mono text-sm text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-gray-700">
              {result.final_evaluation.report}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};