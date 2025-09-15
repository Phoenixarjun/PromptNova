"use client"
import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import  Navbar  from '@/components/Navbar';
import  Footer  from '@/components/Footer';
import guideData from '@/data/guide-details.json';

const GuidePage = () => {
  const [activeTab, setActiveTab] = useState("types");

  const types = guideData.types;
  const frameworks = guideData.frameworks;

  return (
    <div className="flex flex-col min-h-screen bg-gray-50 text-gray-800">
      <Navbar />
      <main className="flex-grow p-6 md:p-10">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-8 text-gray-900 tracking-tight">
            Prompting Guide
          </h1>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 bg-gray-200 p-1 rounded-lg">
              <TabsTrigger
                value="types"
                className="data-[state=active]:bg-white data-[state=active]:text-gray-900 data-[state=active]:shadow-md text-gray-600"
              >
                Types
              </TabsTrigger>
              <TabsTrigger
                value="frameworks"
                className="data-[state=active]:bg-white data-[state=active]:text-gray-900 data-[state=active]:shadow-md text-gray-600"
              >
                Frameworks
              </TabsTrigger>
            </TabsList>
            <TabsContent value="types">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                {types.map((type) => (
                  <Link href={`/guide/${type.slug}`} key={type.name} className="block group">
                    <Card className="bg-white border-gray-200 group-hover:border-blue-500 group-hover:shadow-lg transition-all duration-200 cursor-pointer h-full flex flex-col">
                      <CardHeader>
                        <CardTitle className="text-xl text-gray-900">{type.name}</CardTitle>
                      </CardHeader>
                      <CardContent className="flex-grow">
                        <p className="text-gray-600 text-sm">{type.short_description}</p>
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>
            </TabsContent>
            <TabsContent value="frameworks">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                {frameworks.map((framework) => (
                  <Link href={`/guide/${framework.slug}`} key={framework.name} className="block group">
                    <Card className="bg-white border-gray-200 group-hover:border-blue-500 group-hover:shadow-lg transition-all duration-200 cursor-pointer h-full flex flex-col">
                      <CardHeader>
                        <CardTitle className="text-xl text-gray-900">{framework.name}</CardTitle>
                      </CardHeader>
                      <CardContent className="flex-grow">
                        <p className="text-gray-600 text-sm">{framework.short_description}</p>
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