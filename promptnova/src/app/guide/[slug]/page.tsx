import { notFound } from "next/navigation";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { GuideDetailClient } from "@/components/guide/GuideDetailClient";
import guideData from "@/data/guide-details.json";

const allItems = [...guideData.types, ...guideData.frameworks];

export function generateStaticParams() {
  return allItems
    .filter((item) => item && typeof item.slug === "string")
    .map((item) => ({ slug: item.slug }));
}

// PageProps with async params
interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function DetailPage({ params }: PageProps) {
  const { slug } = await params; // unwrap the Promise
  const item = allItems.find((i) => i.slug === slug);

  if (!item) notFound();

  return (
    <div className="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
      <Navbar />
      <main className="flex-grow p-6 md:p-10">
        <div className="max-w-4xl mx-auto">
          <Link
            href="/guide"
            className="text-gray-500 hover:text-gray-900 mb-8 inline-block"
          >
            &larr; Back to Guide
          </Link>
          <GuideDetailClient item={item} />
        </div>
      </main>
      <Footer />
    </div>
  );
}
