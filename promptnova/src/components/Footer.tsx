import Link from "next/link";
import { Button } from "@/components/ui/button";

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-100 py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center space-y-4 md:flex-row md:justify-between">
          <div className="text-lg font-semibold text-gray-800">
            PromptNova &copy; {new Date().getFullYear()}
          </div>

          <div className="flex space-x-4">
            <Button variant="link" asChild>
              <Link href="/privacy" className="text-gray-600 hover:text-blue-600">
                Privacy Policy
              </Link>
            </Button>
            <Button variant="link" asChild>
              <Link href="/terms" className="text-gray-600 hover:text-blue-600">
                Terms of Service
              </Link>
            </Button>
            <Button variant="link" asChild>
              <Link href="/contact" className="text-gray-600 hover:text-blue-600">
                Contact
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;