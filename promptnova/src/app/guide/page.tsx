"use client";

import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import guideData from '@/data/guide-details.json';

const GuidePage = () => {
  const [activeTab, setActiveTab] = useState('types');
  const { types, frameworks } = guideData;

  return (
    <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
      <Navbar />
      <main className="flex-grow p-6 md:p-10">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-8 text-gray-900 dark:text-white tracking-tight">
            Prompting Guide
          </h1>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 bg-gray-200 dark:bg-gray-800 p-1 rounded-lg">
              <TabsTrigger
                value="types"
                className="data-[state=active]:bg-white dark:data-[state=active]:bg-gray-700 data-[state=active]:text-gray-900 dark:data-[state=active]:text-white data-[state=active]:shadow-md text-gray-600 dark:text-gray-400"
              >
                Types
              </TabsTrigger>
              <TabsTrigger
                value="frameworks"
                className="data-[state=active]:bg-white dark:data-[state=active]:bg-gray-700 data-[state=active]:text-gray-900 dark:data-[state=active]:text-white data-[state=active]:shadow-md text-gray-600 dark:text-gray-400"
              >
                Frameworks
              </TabsTrigger>
            </TabsList>
            <TabsContent value="types">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                {types.map((type) => (
                  <Link key={type.name} href={`/guide/${type.slug}`} className="block group">
                    <Card className="bg-white dark:bg-gray-800/50 border-gray-200 dark:border-gray-700 group-hover:border-blue-500 dark:group-hover:border-blue-400 group-hover:shadow-lg transition-all duration-200 cursor-pointer h-full flex flex-col">
                      <CardHeader>
                        <CardTitle className="text-xl text-gray-900 dark:text-gray-100">{type.name}</CardTitle>
                      </CardHeader>
                      <CardContent className="flex-grow">
                        <p className="text-gray-600 dark:text-gray-400 text-sm">{type.short_description}</p>
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>
            </TabsContent>
            <TabsContent value="frameworks">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                {frameworks.map((framework) => (
                  <Link key={framework.name} href={`/guide/${framework.slug}`} className="block group">
                    <Card className="bg-white dark:bg-gray-800/50 border-gray-200 dark:border-gray-700 group-hover:border-blue-500 dark:group-hover:border-blue-400 group-hover:shadow-lg transition-all duration-200 cursor-pointer h-full flex flex-col">
                      <CardHeader>
                        <CardTitle className="text-xl text-gray-900 dark:text-gray-100">{framework.name}</CardTitle>
                      </CardHeader>
                      <CardContent className="flex-grow">
                        <p className="text-gray-600 dark:text-gray-400 text-sm">{framework.short_description}</p>
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default GuidePage;