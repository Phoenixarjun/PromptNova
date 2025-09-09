"use client"
import React from 'react';
import  Navbar  from '@/components/Navbar';
import  Footer  from '@/components/Footer';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const types = [
    { name: "Zero Shot", description: "Directly provides solutions without examples or reasoning.", slug: "zero_shot" },
    { name: "Chain of Thought (CoT)", description: "Guides step-by-step reasoning for complex problem-solving.", slug: "cot" },
    { name: "One Shot", description: "Uses a single example to guide the solution process.", slug: "one_shot" },
    { name: "Tree of Thought (ToT)", description: "Explores multiple reasoning paths for optimal solutions.", slug: "tot" },
    { name: "ReAct", description: "Combines reasoning and acting for interactive problem-solving.", slug: "react" },
    { name: "In Context", description: "Leverages context from prior interactions for responses.", slug: "in_context" },
    { name: "Emotion", description: "Incorporates emotional context into responses.", slug: "emotion" },
    { name: "Role", description: "Adapts responses based on a defined role or persona.", slug: "role" },
    { name: "Few Shot", description: "Uses multiple examples to guide the solution.", slug: "few_shot" },
    { name: "Self Consistency", description: "Ensures consistent reasoning across multiple attempts.", slug: "self_consistency" },
    { name: "Meta Prompting", description: "Generates prompts to improve subsequent responses.", slug: "meta_prompting" },
    { name: "Least to Most", description: "Solves problems from simplest to most complex steps.", slug: "least_to_most" },
    { name: "Multi Task", description: "Handles multiple tasks within a single prompt.", slug: "multi_task" },
    { name: "Task Decomposition", description: "Breaks tasks into subtasks for structured solutions.", slug: "task_decomposition" },
    { name: "Constrained", description: "Applies constraints to guide the response format.", slug: "constrained" },
    { name: "Generated Knowledge", description: "Generates knowledge to enhance problem-solving.", slug: "generated_knowledge" },
    { name: "Automatic Prompt Engineering", description: "Automates the creation of optimized prompts.", slug: "automatic_prompt_engineering" },
    { name: "Directional Stimulus", description: "Guides responses with directional hints.", slug: "directional_stimulus" }
];

const frameworks = [
    { name: "CoStar", description: "Collaborative strategy framework.", slug: "co_star" },
    { name: "Tcef", description: "Task-centric evaluation framework.", slug: "tcef" },
    { name: "Crispe", description: "Clear, relevant, insightful, simple, precise, effective framework.", slug: "crispe" },
    { name: "Rtf", description: "Role-task-format framework for prompt engineering.", slug: "rtf" },
    { name: "Ice", description: "Iterative, contextual, effective framework.", slug: "ice" },
    { name: "Craft", description: "Creative, refined, actionable, focused, tailored framework.", slug: "craft" },
    { name: "Ape", description: "Automatic prompt engineering framework.", slug: "ape" },
    { name: "Pecra", description: "Precision, efficiency, clarity, relevance, adaptability framework.", slug: "pecra" },
    { name: "Oscar", description: "Optimized, structured, actionable, refined framework.", slug: "oscar" },
    { name: "Rasce", description: "Reasoning, analysis, synthesis, correction, evaluation framework.", slug: "rasce" },
    { name: "Reflection", description: "Reflective learning and adjustment framework.", slug: "reflection" },
    { name: "Flipped Interaction", description: "Reverses traditional interaction patterns.", slug: "flipped_interaction" },
    { name: "Bab", description: "Build, analyze, balance framework.", slug: "bab" }
];


interface DetailPageProps {
  params: {
    slug: string;
  };
}

const DetailPage = ({ params }: DetailPageProps) => {
  const { slug } = params;
  const item = [...types, ...frameworks].find((i) => i.slug === slug);

  if (!item) {
    return (
      <div className="flex flex-col min-h-screen bg-gray-900 text-white">
        <Navbar />
        <main className="flex-grow flex items-center justify-center p-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">Not Found</h1>
            <p className="text-gray-400">The requested guide page could not be found.</p>
            <Link href="/guide" className="mt-6 inline-block bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded">
              Back to Guide
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      <Navbar />
      <main className="flex-grow p-6 md:p-10">
        <div className="max-w-4xl mx-auto">
          <Link href="/guide" className="text-gray-400 hover:text-white mb-8 inline-block">
            &larr; Back to Guide
          </Link>
          <Card className="bg-gray-800 border-gray-700">
            <CardHeader>
              <CardTitle className="text-4xl md:text-5xl font-extrabold text-white tracking-tight">
                {item.name}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg text-gray-300 mt-4">
                {item.description}
              </p>
              {/* Here you could add more detailed information, examples, etc. */}
            </CardContent>
          </Card>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default DetailPage;