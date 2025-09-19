import React from 'react'

export const HeroSection: React.FC = () => {
  return (
    <div className="relative overflow-hidden bg-gray-900 shadow-2xl">
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 opacity-95"></div>
      <div className="absolute inset-0 mix-blend-overlay bg-gradient-radial from-gray-700/40 via-gray-800/30 to-gray-900/80"></div>
      <div className="relative max-w-4xl mx-auto text-center py-24 px-4 sm:py-32 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl md:text-6xl">
          <span className="block">Unlock the Power of AI</span>
          <span className="block text-4xl text-gray-300">with Precision Prompts</span>
        </h1>
        <p className="mt-6 max-w-lg mx-auto text-xl text-gray-400 sm:max-w-3xl">
          Welcome to PromptNova. Craft, refine, and optimize your prompts to get the best results from any language model.
        </p>
      </div>
    </div>
  )
}
