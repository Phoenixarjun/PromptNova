import React from 'react';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import guideData from '@/data/guide-details.json'
import { CheckCircle2, Clipboard, Check } from 'lucide-react';

const allItems = [...guideData.types, ...guideData.frameworks];
interface DetailPageProps {
  params: {
    slug: string;
  };
}

// This is the Client Component responsible for rendering the detailed view.
// It receives the resolved `item` data as a prop.
const GuideDetailView = ({ item }: { item: typeof allItems[0] }) => {
  "use client";
  const [copiedIndex, setCopiedIndex] = React.useState<number | null>(null);

  const handleCopy = (text: string, index: number) => {
    // We only want to copy the "User Prompt" part for practical use.
    const promptToCopy = text.split('\n')[0].replace('User Prompt: ', '');
    navigator.clipboard.writeText(promptToCopy).then(() => {
      setCopiedIndex(index);
      setTimeout(() => {
        setCopiedIndex(null);
      }, 2000); // Reset after 2 seconds
    });
  };
  return (
    <div className="flex flex-col min-h-screen bg-gray-50 text-gray-800">
      <Navbar />
      <main className="flex-grow p-6 md:p-10">
        <div className="max-w-4xl mx-auto">
          <Link href="/guide" className="text-gray-500 hover:text-gray-900 mb-8 inline-block">
            &larr; Back to Guide
          </Link>
          <Card className="bg-white border-gray-200 shadow-lg">
            <CardHeader>
              <CardTitle className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight">
                {item.name}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-lg text-gray-600 mt-4 leading-relaxed">
                {item.description}
              </p>

              <div className="mt-8">
                <h3 className="text-2xl font-bold text-gray-800 mb-4">Examples</h3>
                <div className="space-y-4">
                  {item.examples.map((example, index) => (
                    <div key={index} className="relative group">
                      <blockquote className="border-l-4 border-blue-500 bg-gray-100 p-4 rounded-r-lg pr-12">
                        <p className="text-gray-700 whitespace-pre-wrap font-mono text-sm">{example}</p>
                      </blockquote>
                      <button
                        onClick={() => handleCopy(example, index)}
                        className="absolute top-2 right-2 p-1.5 bg-gray-200 text-gray-600 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-gray-300"
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
                <h3 className="text-2xl font-bold text-gray-800 mb-4">Advantages</h3>
                <ul className="space-y-3">
                  {item.advantages.map((advantage, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle2 className="flex-shrink-0 h-5 w-5 text-green-500 mr-3 mt-1" />
                      <span className="text-gray-700">{advantage}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
      <Footer />
    </div>
  );
};

const DetailPage = ({ params }: DetailPageProps) => {
  const { slug } = params;
  const item = allItems.find((i) => i.slug === slug);

  // Data fetching and routing logic is handled on the server.
  if (!item) {
    // Render the "Not Found" UI from the server.
    return (
      <div className="flex flex-col min-h-screen bg-gray-50 text-gray-800">
        <Navbar />
        <main className="flex-grow flex items-center justify-center p-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">Not Found</h1>
            <p className="text-gray-500">The requested guide page could not be found.</p>
            <Link href="/guide" className="mt-6 inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Back to Guide
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  // Pass the resolved data to the client component for rendering.
  return <GuideDetailView item={item} />;
};

export default DetailPage;