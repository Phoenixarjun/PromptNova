"use client";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const AboutPage = () => {
  return (
    <div className='flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900'>
      <Navbar />
        <main className='flex-grow p-6 md:p-10'>
          <div className="max-w-4xl mx-auto w-full">
            <section className='w-full flex-center flex-col animate-fadeIn'>
              <h1 className='text-4xl md:text-5xl font-extrabold mb-4 text-center text-gray-900 dark:text-white tracking-tight animate-fadeIn'>
                About <span className='blue_gradient'>PromptNova</span>
              </h1>
              <p className='text-lg text-gray-600 dark:text-gray-400 text-center max-w-4xl animate-fadeIn animation-delay-100'>
                Tackling AI&apos;s &quot;Performance Under-Supply&quot; by unlocking the true potential of language models through advanced prompt engineering.
              </p>

              <div className='mt-16 w-full flex flex-col gap-16'>
                {/* Mission & Vision Section */}
                <div className='bg-white/50 dark:bg-black/20 backdrop-blur-sm p-6 rounded-lg animate-fadeIn animation-delay-200'>
                  <h2 className='text-2xl font-satoshi font-bold text-gray-900 dark:text-gray-100'>
                    The Problem: Performance Under-Supply (PUX)
                  </h2>
                  <p className='mt-3 font-satoshi text-gray-600 dark:text-gray-300'>
                    After using AI for some time, I realized that creating truly expert-level agents took significant effort. While Large Language Models (LLMs) are incredibly powerful, most of us are unaware of the vast array of prompt engineering <span className="font-semibold text-gray-700 dark:text-gray-200">types and frameworks</span> that exist.
                  </p>
                  <p className='mt-3 font-satoshi text-gray-600 dark:text-gray-300'>
                    This leads to what I call <span className="font-semibold text-gray-700 dark:text-gray-200">&quot;Performance Under-Supply&quot; (PUX)</span> where we only tap into a fraction of an AI&apos;s true potential. These advanced techniques can unlock over 90% of a model&apos;s capability, making it easier to create custom, expert agents for any task.
                  </p>
                </div>

                {/* The PromptNova Solution */}
                <div className='animate-fadeIn animation-delay-300'>
                  <h2 className='text-2xl font-satoshi font-bold text-gray-900 dark:text-gray-100'>
                    The PromptNova Solution
                  </h2>
                  <p className='mt-3 font-satoshi text-gray-600 dark:text-gray-300'>
                    PromptNova is more than just a simple workflow. In the background, it implements advanced techniques like <span className="font-semibold text-gray-700 dark:text-gray-200">Context Engineering and EvalLoop</span> to ensure you get the exact results you want. Modern LLMs often use a &quot;Mixture of Experts&quot; (MoE) architecture, where different internal &quot;experts&quot; handle different tasks. By providing a well-structured prompt, you can activate the right experts and unlock the full potential of the AI.
                  </p>
                  <p className='mt-3 font-satoshi text-gray-600 dark:text-gray-300'>
                    This tool is designed to help you build that structure, setting a solid base for your AI agent so it has a clear role and stays on track.
                  </p>
                </div>

                {/* What Can You Do Section */}
                <div className='animate-fadeIn animation-delay-400'>
                  <h2 className='text-2xl font-satoshi font-bold text-gray-900 dark:text-gray-100'>
                    What Can You Do?
                  </h2>
                  <div className='mt-6 grid grid-cols-1 md:grid-cols-3 gap-6'>
                    <div className='flex flex-col gap-2 bg-white/50 dark:bg-black/20 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow duration-300'>
                      <h3 className='font-semibold text-gray-800 dark:text-gray-200'>Create Expert-Lens Prompts</h3>
                      <p className='text-sm text-gray-600 dark:text-gray-400'>Use our tools to build highly specialized prompts that act as &quot;expert agents&quot; for any task, from coding to creative writing.</p>
                    </div>
                    <div className='flex flex-col gap-2 bg-white/50 dark:bg-black/20 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow duration-300'>
                      <h3 className='font-semibold text-gray-800 dark:text-gray-200'>Learn with the Guide</h3>
                      <p className='text-sm text-gray-600 dark:text-gray-400'>Explore our comprehensive <Link href="/guide" className="text-blue-600 dark:text-blue-400 hover:underline">Guide</Link> to understand the different types and frameworks of prompt engineering.</p>
                    </div>
                    <div className='flex flex-col gap-2 bg-white/50 dark:bg-black/20 p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow duration-300'>
                      <h3 className='font-semibold text-gray-800 dark:text-gray-200'>Go Deep with Expert Mode</h3>
                      <p className='text-sm text-gray-600 dark:text-gray-400'>Switch to Expert Mode to fine-tune every detail of your prompt strategy, giving you granular control over the AI&apos;s output.</p>
                    </div>
                  </div>
                </div>

                {/* A Note on AI & Patience */}
                <div className='bg-white/50 dark:bg-black/20 backdrop-blur-sm p-6 rounded-lg animate-fadeIn animation-delay-500'>
                  <h2 className='text-2xl font-satoshi font-bold text-gray-900 dark:text-gray-100'>
                    A Note on AI &amp; Patience
                  </h2>
                  <p className='mt-3 font-satoshi text-gray-600 dark:text-gray-300'>
                    One thing to understand is that AI is not perfectly deterministic. Even with the same settings, you might not get the exact same output every time. After many days of testing, PromptNova works perfectly most of the time, but occasionally, output parsing can cause issues.
                  </p>
                  <p className='mt-3 font-satoshi font-semibold text-gray-700 dark:text-gray-200'>
                    If a result doesn&apos;t meet your goal, please be patient. Try running it again, or use the <span className="italic">Refine</span> feature. A little patience (and maybe a cup of coffee) goes a long way!
                  </p>
                </div>

                {/* Our Story Section */}
                <div className='animate-fadeIn animation-delay-600'>
                  <h2 className='text-2xl font-satoshi font-bold text-gray-900 dark:text-gray-100'>
                    Our Story
                  </h2>
                  <p className='mt-3 font-satoshi text-gray-600 dark:text-gray-300'>
                    PromptNova is a project I started to help others get the best prompts, and also for me to learn and try different things and techniques I&apos;ve read about. It began as a personal project to better understand the full-stack development process with Next.js, and I was fascinated by the potential of AI. I realized that the quality of an AI&apos;s output depends entirely on the prompt, and this project quickly grew into a passion for building a community around prompt engineering.
                  </p>
                  <p className='mt-4 font-satoshi text-gray-600 dark:text-gray-300'>
                    Hi, I&apos;m <span className='font-bold'>NARESH B A</span>, a software developer passionate about building modern web applications and exploring the intersection of technology and creativity. You can check out more of my work on my{" "}
                    <a href="https://naresh-portfolio-007.netlify.app/" target="_blank" rel="noopener noreferrer" className='orange_gradient font-semibold hover:underline'>
                      portfolio
                    </a>.
                  </p>
                </div>

                {/* Get in Touch Section */}
                <div className='text-center p-6 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 animate-fadeIn animation-delay-700'>
                  <h2 className='text-2xl font-satoshi font-bold text-gray-900 dark:text-gray-100'>
                    Get in Touch &amp; Contribute
                  </h2>
                  <p className='mt-3 font-satoshi text-gray-600 dark:text-gray-300'>
                    Have a suggestion or found a bug? I&apos;d love to hear from you! Feel free to reach out at{" "}
                    <a href="mailto:naresh.b.a2003@gmail.com" className='font-semibold text-primary-orange hover:underline'>
                      naresh.b.a2003@gmail.com
                    </a>.
                  </p>
                  <p className='mt-2 font-satoshi text-gray-600 dark:text-gray-300'>
                    PromptNova is an open-source project! If you&apos;re a developer interested in contributing, please check out the{" "}
                    <Link href="https://github.com/Phoenixarjun/PromptNova" target="_blank" rel="noopener noreferrer" className='font-semibold text-primary-orange hover:underline'>
                      GitHub Repository
                    </Link>. Pull requests are always welcome!
                  </p>
                </div>
              </div>
            </section>
          </div>
        </main>
      <Footer />
    </div>
  );
};

export default AboutPage;