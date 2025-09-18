"use client";

import { useState } from 'react';
import  Footer  from '@/components/Footer';
import { Form } from '@/components/Home/Form';
import { HeroSection } from '@/components/Home/HeroSection';
import { Sidebar } from '@/components/Home/Sidebar';
import Navbar from '@/components/Navbar';

export default function Home() {
  const [result, setResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <div className="flex flex-1 flex-col md:flex-row">
        <Sidebar />
        <main className="flex-1 bg-gray-50">
          <HeroSection />
          <Form
            result={result}
            setResult={setResult}
            setIsLoading={setIsLoading}
            setError={setError}
            isLoading={isLoading}
            error={error}
          />
        </main>
      </div>
      <Footer />
    </div>
  );
}