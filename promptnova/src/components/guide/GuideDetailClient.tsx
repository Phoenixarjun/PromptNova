"use client"

import React from 'react';
import { CheckCircle2, Clipboard, Check } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

// Define the type for a single guide item
type GuideItem = {
  name: string;
  slug: string;
  description: string;
  examples: string[];
  advantages: string[];
};

export const GuideDetailClient = ({ item }: { item: GuideItem }) => {
  const [copiedIndex, setCopiedIndex] = React.useState<number | null>(null);

  const handleCopy = (text: string, index: number) => {
    const promptToCopy = text.split('\n')[0].replace('User Prompt: ', '');
    navigator.clipboard.writeText(promptToCopy).then(() => {
      setCopiedIndex(index);
      setTimeout(() => {
        setCopiedIndex(null);
      }, 2000);
    });
  };

  return (
    <Card className="bg-white dark:bg-gray-800/50 border-gray-200 dark:border-gray-700 shadow-lg">
      <CardHeader>
        <CardTitle className="text-4xl md:text-5xl font-extrabold text-gray-900 dark:text-gray-100 tracking-tight">
          {item.name}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-lg text-gray-600 dark:text-gray-400 mt-4 leading-relaxed">
          {item.description}
        </p>

        <div className="mt-8">
          <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">Examples</h3>
          <div className="space-y-4">
            {item.examples.map((example, index) => (
              <div key={index} className="relative group">
                <blockquote className="border-l-4 border-blue-500 bg-gray-100 dark:bg-gray-800 p-4 rounded-r-lg pr-12">
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-mono text-sm">{example}</p>
                </blockquote>
                <button
                  onClick={() => handleCopy(example, index)}
                  className="absolute top-2 right-2 p-1.5 bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-gray-300 dark:hover:bg-gray-600"
                  aria-label="Copy prompt"
                >
                  {copiedIndex === index ? (
                    <Check className="h-4 w-4 text-green-600" />
                  ) : (
                    <Clipboard className="h-4 w-4" />
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>
        <div className="mt-8">
          <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">Advantages</h3>
          <ul className="space-y-3">
            {item.advantages.map((advantage, index) => (
              <li key={index} className="flex items-start">
                <CheckCircle2 className="flex-shrink-0 h-5 w-5 text-green-500 mr-3 mt-1" />
                <span className="text-gray-700 dark:text-gray-300">{advantage}</span>
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  );
};