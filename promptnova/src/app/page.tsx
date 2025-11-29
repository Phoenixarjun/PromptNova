"use client";

import { useState } from 'react';
import Footer from '@/components/Footer';
import { Form } from '@/components/Home/Form';
import { HeroSection } from '@/components/Home/HeroSection';
import { ResultDisplay } from '@/components/Home/ResultDisplay';
import { Sidebar } from '@/components/Home/Sidebar';
import Navbar from '@/components/Navbar';

export default function Home() {
  const [result, setResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedModel, setSelectedModel] = useState('gemini');
  const [selectedGroqModel, setSelectedGroqModel] = useState('llama3-8b-8192');

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
        <main className="flex-1 bg-gray-50 dark:bg-gray-800/50">
          <HeroSection />
          <div className='p-10'>
          <Form
            result={result}
            setResult={setResult}
            setIsLoading={setIsLoading}
            setError={setError}
            isLoading={isLoading}
            selectedModel={selectedModel}
            selectedGroqModel={selectedGroqModel}
          />
          <ResultDisplay result={result} isLoading={isLoading} error={error} />
          </div>

        </main>
      </div>
      <Footer />
    </div>
  );
}