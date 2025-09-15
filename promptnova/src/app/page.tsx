import Footer from "@/components/Footer";
import { Form } from "@/components/Home/Form";
import { HeroSection } from "@/components/Home/HeroSection";
import { Sidebar } from "@/components/Home/Sidebar";
import Navbar from "@/components/Navbar";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <div className="flex flex-1 flex-col md:flex-row">
        <Sidebar />
        <main className="flex-1 bg-gray-50">
          <HeroSection />
          <Form />
        </main>
      </div>
      <Footer />
    </div>
  );
}
