import React from 'react'

export const HeroSection : React.FC = () => {
  return (
    <div className='flex flex-col justify-center items-center py-20 px-4 bg-gray-900 text-white shadow-lg border-b border-gray-700'>
      <h1 className='text-5xl md:text-6xl font-extrabold mb-4 tracking-tight'>
        Prompt Nova
      </h1>
      <p className='text-xl md:text-2xl text-gray-300'>AI Prompt Generator for Developers</p>
    </div>
  )
}
