"use client";

import React from 'react';
import { Textarea } from '@/components/ui/textarea';

interface FormFieldProps {
  id: string;
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder: string;
  required?: boolean;
  helperText?: string;
  minHeight?: string;
}

export const FormField: React.FC<FormFieldProps> = ({
  id,
  label,
  value,
  onChange,
  placeholder,
  required = false,
  helperText,
  minHeight = 'min-h-[150px]',
}) => (
  <div>
    <label htmlFor={id} className="block text-gray-700 dark:text-gray-300 text-sm font-semibold mb-2">
      {label} {required && <span className="text-red-500">*</span>}
    </label>
    <Textarea id={id} value={value} onChange={onChange} placeholder={placeholder} className={`w-full p-3 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 resize-y ${minHeight}`} required={required} />
    {helperText && <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{helperText}</p>}
  </div>
);