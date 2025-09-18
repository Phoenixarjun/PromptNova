"use client";

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check } from 'lucide-react';

interface MarkdownRendererProps {
  content: string;
}

const CodeBlock: React.FC<any> = ({ node, inline, className, children, ...props }) => {
  const [isCopied, setIsCopied] = useState(false);
  const match = /language-(\w+)/.exec(className || '');
  const codeString = String(children).replace(/\n$/, '');

  const handleCopy = () => {
    navigator.clipboard.writeText(codeString);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  return !inline && match ? (
    <div className="relative my-4 rounded-md bg-gray-800 text-white font-mono text-sm">
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-700">
        <span className="text-xs font-sans text-gray-400">{match[1]}</span>
        <button
          onClick={handleCopy}
          className="inline-flex items-center gap-1.5 text-xs text-gray-400 hover:text-white transition-colors"
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
    <code className="bg-gray-200 text-gray-800 rounded-sm px-1.5 py-1 font-mono text-sm" {...props}>
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
          h1: ({node, ...props}) => <h1 className="text-3xl font-bold mt-8 mb-4 text-gray-900" {...props} />,
          h2: ({node, ...props}) => <h2 className="text-2xl font-bold mt-6 mb-3 border-b pb-2 text-gray-800" {...props} />,
          h3: ({node, ...props}) => <h3 className="text-xl font-semibold mt-4 mb-2 text-gray-800" {...props} />,
          p: ({node, ...props}) => <p className="leading-7 my-4 text-gray-700" {...props} />,
          ul: ({node, ...props}) => <ul className="list-disc pl-6 my-4 space-y-2" {...props} />,
          li: ({node, ...props}) => <li className="pl-2 text-gray-700" {...props} />,
          strong: ({node, ...props}) => <strong className="font-bold text-gray-800" {...props} />,
          blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-gray-300 pl-4 italic text-gray-600" {...props} />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

