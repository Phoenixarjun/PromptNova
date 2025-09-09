"use client"
import React, { useState } from 'react';

export const Form = () => {
  const types = [
    { name: "Zero Shot", slug: "zero_shot" },
    { name: "Chain of Thought (CoT)", slug: "cot" },
    { name: "One Shot", slug: "one_shot" },
    { name: "Tree of Thought (ToT)", slug: "tot" },
    { name: "ReAct", slug: "react" },
    { name: "In Context", slug: "in_context" },
    { name: "Emotion", slug: "emotion" },
    { name: "Role", slug: "role" },
    { name: "Few Shot", slug: "few_shot" },
    { name: "Self Consistency", slug: "self_consistency" },
    { name: "Meta Prompting", slug: "meta_prompting" },
    { name: "Least to Most", slug: "least_to_most" },
    { name: "Multi Task", slug: "multi_task" },
    { name: "Task Decomposition", slug: "task_decomposition" },
    { name: "Constrained", slug: "constrained" },
    { name: "Generated Knowledge", slug: "generated_knowledge" },
    { name: "Automatic Prompt Engineering", slug: "automatic_prompt_engineering" },
    { name: "Directional Stimulus", slug: "directional_stimulus" }
  ];

  const frameworks = [
    { name: "CoStar", slug: "co_star" },
    { name: "Tcef", slug: "tcef" },
    { name: "Crispe", slug: "crispe" },
    { name: "Rtf", slug: "rtf" },
    { name: "Ice", slug: "ice" },
    { name: "Craft", slug: "craft" },
    { name: "Ape", slug: "ape" },
    { name: "Pecra", slug: "pecra" },
    { name: "Oscar", slug: "oscar" },
    { name: "Rasce", slug: "rasce" },
    { name: "Reflection", slug: "reflection" },
    { name: "Flipped Interaction", slug: "flipped_interaction" },
    { name: "Bab", slug: "bab" }
  ];

  const [promptText, setPromptText] = useState('');
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [selectedFramework, setSelectedFramework] = useState<string | null>(null);

  const handleTypeToggle = (slug: string) => {
    setSelectedTypes(prev =>
      prev.includes(slug) ? prev.filter(s => s !== slug) : [...prev, slug]
    );
  };

  const handleFrameworkSelect = (slug: string) => {
    setSelectedFramework(prev => (prev === slug ? null : slug));
  };

  const handleRemoveSelected = (slug: string, type: 'type' | 'framework') => {
    if (type === 'type') {
      setSelectedTypes(prev => prev.filter(s => s !== slug));
    } else {
      setSelectedFramework(null);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Prompt:', promptText);
    console.log('Selected Types:', selectedTypes);
    console.log('Selected Framework:', selectedFramework);
    // Here you would typically send this data to your backend API
  };

  return (
    <div className="p-8 bg-gray-50 rounded-lg shadow-md max-w-3xl mx-auto my-8 border border-gray-200">
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label htmlFor="prompt-input" className="block text-gray-700 text-sm font-semibold mb-2">
            Enter Your Prompt
          </label>
          <textarea
            id="prompt-input"
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 bg-white text-gray-800 resize-y min-h-[120px]"
            value={promptText}
            onChange={(e) => setPromptText(e.target.value)}
            placeholder="e.g., Generate a Python function to calculate Fibonacci sequence."
          />
        </div>

        <div className="mb-6">
          <h2 className="text-gray-700 text-sm font-semibold mb-3">Select Prompt Types (Multiple)</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {types.map(type => (
              <button
                key={type.slug}
                type="button"
                onClick={() => handleTypeToggle(type.slug)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200
                  ${selectedTypes.includes(type.slug)
                    ? 'bg-gray-800 text-white border border-gray-800'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-100'
                  }`}
              >
                {type.name}
              </button>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h2 className="text-gray-700 text-sm font-semibold mb-3">Select Framework (Single)</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {frameworks.map(framework => (
              <button
                key={framework.slug}
                type="button"
                onClick={() => handleFrameworkSelect(framework.slug)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200
                  ${selectedFramework === framework.slug
                    ? 'bg-gray-800 text-white border border-gray-800'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-100'
                  }`}
              >
                {framework.name}
              </button>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <h2 className="text-gray-700 text-sm font-semibold mb-3">Selected Options</h2>
          <div className="flex flex-wrap gap-2">
            {selectedTypes.map(slug => (
              <span key={slug} className="bg-gray-200 text-gray-800 px-3 py-1 rounded-full flex items-center gap-1 text-sm">
                {types.find(t => t.slug === slug)?.name || slug}
                <button
                  type="button"
                  onClick={() => handleRemoveSelected(slug, 'type')}
                  className="text-gray-600 hover:text-gray-900 ml-1"
                >
                  &times;
                </button>
              </span>
            ))}
            {selectedFramework && (
              <span className="bg-gray-200 text-gray-800 px-3 py-1 rounded-full flex items-center gap-1 text-sm">
                {frameworks.find(f => f.slug === selectedFramework)?.name || selectedFramework}
                <button
                  type="button"
                  onClick={() => handleRemoveSelected(selectedFramework, 'framework')}
                  className="text-gray-600 hover:text-gray-900 ml-1"
                >
                  &times;
                </button>
              </span>
            )}
            {selectedTypes.length === 0 && !selectedFramework && (
              <p className="text-gray-500 text-sm">No options selected yet.</p>
            )}
          </div>
        </div>

        <button
          type="submit"
          className="w-full bg-gray-800 text-white px-6 py-3 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 font-semibold text-lg"
        >
          Generate Prompt
        </button>
      </form>
    </div>
  )
}
