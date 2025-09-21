"use client"
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import Link from "next/link";
import { Menu } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";
import Image from "next/image";

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const navLinks = [
    { name: "Home", href: "/" },
    { name: "Guide", href: "/guide" },
    { name: "About", href: "/about" },
  ];

  return (
    <nav className="bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/" className="flex items-center">
                <Image src="/Icon.png" alt="Icon" width={60} height={60}></Image>


            <span className="text-3xl font-bold bg-gradient-to-r from-gray-700 via-gray-600 to-gray-800 dark:from-gray-300 via-gray-200 to-gray-100 text-transparent bg-clip-text dark:p-[1px] dark:[-webkit-text-stroke:0.3px_white] dark:[text-stroke:0.3px_white]">
              PromptNova
            </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <div className="flex items-center space-x-1 bg-white dark:bg-gray-800 rounded-full px-2 py-1 shadow-sm">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  className="text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 px-4 py-2 rounded-full text-sm font-medium transition-colors"
                >
                  {link.name}
                </Link>
              ))}
            </div>
            <ThemeToggle />
          </div>

          {/* Mobile Menu Button */}
          <div className="flex items-center gap-2 md:hidden">
            <ThemeToggle />
            <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="outline"
                    size="icon"
                    className="bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600"
                  >
                    <Menu className="h-6 w-6" />
                    <span className="sr-only">Toggle menu</span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                  align="end"
                  className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 mt-2 shadow-lg"
                >
                  {navLinks.map((link) => (
                    <DropdownMenuItem
                      key={link.name}
                      className="focus:bg-gray-100 dark:focus:bg-gray-700"
                    >
                      <Link
                        href={link.href}
                        className="w-full text-gray-700 dark:text-gray-300 px-4 py-2"
                        onClick={() => setIsOpen(false)}
                      >
                        {link.name}
                      </Link>
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;