import Footer from "@/components/Footer";
import { Form } from "@/components/Home/Form";
import { HeroSection } from "@/components/Home/HeroSection";
import Navbar from "@/components/Navbar";
import Image from "next/image";

export default function Home() {
  return (
    <div>
      <Navbar />
      <HeroSection />
      <Form />
      <Footer />
    </div>
  );
}
