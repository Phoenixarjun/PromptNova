"use client"
import React from "react"
import { ChevronDown } from "lucide-react"

export const HeroSection: React.FC = () => {
  const handleScroll = () => {
    window.scrollTo({
      top: window.innerHeight,
      behavior: "smooth",
    })
  }

  return (
    <section className="relative overflow-hidden transition-colors duration-500 bg-gradient-to-br from-gray-100 via-gray-50 to-white dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 shadow-2xl">
      {/* Gradient overlays */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-200 via-gray-100 to-gray-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 opacity-95"></div>
      <div className="absolute inset-0 mix-blend-overlay bg-gradient-radial from-gray-400/20 via-gray-100/10 to-transparent dark:from-gray-700/40 dark:via-gray-800/30 dark:to-gray-900/80"></div>

      {/* Content */}
      <div className="relative max-w-4xl mx-auto text-center py-24 px-4 sm:py-32 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-extrabold tracking-tight text-gray-700 dark:text-white sm:text-5xl md:text-6xl">
          <span className="block">Unlock the Power of AI</span>
          <span className="block text-4xl text-gray-600 dark:text-gray-300">
            with Precision Prompts
          </span>
        </h1>
        <p className="mt-6 max-w-lg mx-auto text-xl text-gray-600 dark:text-gray-400 sm:max-w-3xl">
          Welcome to <span className="font-semibold text-gray-800 dark:text-gray-200">PromptNova</span> craft, refine, and optimize your prompts effortlessly to get the best results from any language model.
        </p>

        <button
          onClick={handleScroll}
          className="mt-16 inline-flex items-center justify-center w-14 h-14 rounded-full border border-gray-400 dark:border-gray-500 text-gray-700 dark:text-gray-300 hover:text-black dark:hover:text-white hover:border-black dark:hover:border-white transition-all duration-300"
        >
          <ChevronDown size={28} />
        </button>
      </div>
    </section>
  )
}
