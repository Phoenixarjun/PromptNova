"use client";

import { useState } from 'react';
import Footer from '@/components/Footer';
import { ProjectManiaForm } from '@/components/ProjectMania/Form';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import { ProjectManiaResultDisplay } from '@/components/ProjectMania/ProjectManiaResultDisplay';
import { Sidebar } from '@/components/Home/Sidebar';
import Navbar from '@/components/Navbar';

export default function ProjectManiaPage() {
  const [result, setResult] = useState('');
  const [metadata, setMetadata] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedModel, setSelectedModel] = useState('gemini');
  const [selectedGroqModel, setSelectedGroqModel] = useState('llama3-8b-8192');
  const [templateType, setTemplateType] = useState<'general' | 'crewai' | 'autogen'>('general');

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-gray-900">
      <Navbar />
      <div className="flex flex-1 flex-col md:flex-row">
        <Sidebar
          selectedModel={selectedModel}
          setSelectedModel={setSelectedModel}
          selectedGroqModel={selectedGroqModel}
          setSelectedGroqModel={setSelectedGroqModel}
        />
        <main className="flex-1 bg-gray-50 dark:bg-gray-800/50 p-10">
            {/* Hero Section */}
            <div className="text-center space-y-4 mb-12">
              <h1 className='text-5xl font-extrabold text-gray-800 dark:text-gray-100 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent'>
                Project Mania
              </h1>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                Architect complex AI systems with a single blueprint. 
                Generate production-ready templates for CrewAI, AutoGen, and more.
              </p>
            </div>

            {/* Error Alert */}
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Form */}
            <ProjectManiaForm 
              setResult={setResult}
              setMetadata={setMetadata}
              setIsLoading={setIsLoading}
              setError={setError}
              isLoading={isLoading}
              selectedModel={selectedModel}
              selectedGroqModel={selectedGroqModel}
              templateType={templateType}
              setTemplateType={setTemplateType}
            />

            {/* Result Display */}
            <div className="mt-8">
              <ProjectManiaResultDisplay 
                result={result} 
                metadata={metadata} 
                isLoading={isLoading} 
                error={error} 
                templateType={templateType}
              />
            </div>
        </main>
      </div>
      <Footer />
    </div>
  );
}