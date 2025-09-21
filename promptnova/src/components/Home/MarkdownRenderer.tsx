"use client";

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check } from 'lucide-react';

interface MarkdownRendererProps {
  content: string;
}

interface CodeBlockProps {
    node?: unknown;
    inline?: boolean;
    className?: string;
    children?: React.ReactNode;
  }

const CodeBlock: React.FC<CodeBlockProps> = ({ node: _node, inline, className, children, ...props }) => {
  const [isCopied, setIsCopied] = useState(false);
  const match = /language-(\w+)/.exec(className || '');
  const codeString = String(children).replace(/\n$/, '');

  const handleCopy = () => {
    navigator.clipboard.writeText(codeString);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  return !inline && match ? (
    <div className="relative my-4 rounded-md bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-mono text-sm">
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-200 dark:border-gray-700">
        <span className="text-xs font-sans text-gray-500 dark:text-gray-400">{match[1]}</span>
        <button
          onClick={handleCopy}
          className="inline-flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          aria-label="Copy code"
        >
          {isCopied ? (
            <>
              <Check size={14} /> Copied!
            </>
          ) : (
            <>
              <Copy size={14} /> Copy
            </>
          )}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto"><code className={className} {...props}>{children}</code></pre>
    </div>
  ) : (
    <code className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-sm px-1.5 py-1 font-mono text-sm" {...props}>
      {children}
    </code>
  );
};

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  return (
    <div className="prose prose-gray max-w-none dark:prose-invert">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code: CodeBlock,
          h1: ({node: _node, ...props}) => <h1 className="text-3xl font-bold mt-8 mb-4 text-gray-900 dark:text-gray-100" {...props} />,
          h2: ({node: _node, ...props}) => <h2 className="text-2xl font-bold mt-6 mb-3 border-b border-gray-200 dark:border-gray-700 pb-2 text-gray-800 dark:text-gray-200" {...props} />,
          h3: ({node: _node, ...props}) => <h3 className="text-xl font-semibold mt-4 mb-2 text-gray-800 dark:text-gray-200" {...props} />,
          p: ({node: _node, ...props}) => <p className="leading-7 my-4 text-gray-700 dark:text-gray-300" {...props} />,
          ul: ({node: _node, ...props}) => <ul className="list-disc pl-6 my-4 space-y-2" {...props} />,
          li: ({node: _node, ...props}) => <li className="pl-2 text-gray-700 dark:text-gray-300" {...props} />,
          strong: ({node: _node, ...props}) => <strong className="font-bold text-gray-800 dark:text-gray-200" {...props} />,
          blockquote: ({node: _node, ...props}) => <blockquote className="border-l-4 border-gray-300 dark:border-gray-600 pl-4 italic text-gray-600 dark:text-gray-400" {...props} />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};
