"use client"
import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { CardDesign } from "@/components/guide/CardDesign";

const GuidePage = () => {
  const [activeTab, setActiveTab] = useState("types");

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
    { name: "Directional Stimulus", description: "Guides responses with directional hints.", slug: "directional_stimulus" },
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
    { name: "Bab", description: "Build, analyze, balance framework.", slug: "bab" },
  ];

  return (
    <div className="min-h-screen bg-white text-black p-6">
      <h1 className="text-3xl font-semibold mb-6 text-gray-900">Guide</h1>
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 bg-gray-100">
          <TabsTrigger value="types" className="data-[state=active]:bg-white data-[state=active]:text-black">
            Types
          </TabsTrigger>
          <TabsTrigger value="frameworks" className="data-[state=active]:bg-white data-[state=active]:text-black">
            Frameworks
          </TabsTrigger>
        </TabsList>
        <TabsContent value="types">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
            {types.map((type) => (
              <Link href={`/guide/${type.slug}`} key={type.name}>
                <CardDesign type={type} />
              </Link>
            ))}
          </div>
        </TabsContent>
        <TabsContent value="frameworks">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
            {frameworks.map((framework) => (
              <Link href={`/guide/${framework.slug}`} key={framework.name}>
                <CardDesign type={framework} />
              </Link>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default GuidePage;