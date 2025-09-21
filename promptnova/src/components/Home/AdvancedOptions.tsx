import React from 'react';
import { advancedTypeOptions, advancedFrameworkOptions } from './advancedOptionsConfig';

// Define a more specific type for advanced parameters
interface AdvancedParams {
  types?: {
    [key: string]: {
      [key: string]: string;
    };
  };
  framework?: {
    [key: string]: {
      [key: string]: string;
    };
  };
}

interface Field {
  name: string;
  label: string;
  type: 'text' | 'textarea';
  description: string;
}

interface AdvancedOptionsProps {
  selectedTypes: string[];
  selectedFramework: string | null;
  advancedParams: AdvancedParams;
  setAdvancedParams: (params: AdvancedParams | ((prev: AdvancedParams) => AdvancedParams)) => void;
}

const renderField = (field: Field, value: string, onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void) => {
  const commonProps = {
    id: field.name,
    name: field.name,
    value: value || '',
    onChange,
    placeholder: field.description,
    className: "w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-400 dark:focus:ring-gray-500 bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 text-sm"
  };

  if (field.type === 'textarea') {
    return <textarea {...commonProps} rows={2} />;
  }
  return <input type={field.type} {...commonProps} />;
};

export const AdvancedOptions: React.FC<AdvancedOptionsProps> = ({
  selectedTypes,
  selectedFramework,
  advancedParams,
  setAdvancedParams,
}) => {
  const handleTypeChange = (typeSlug: string, fieldName: string, value: string) => {
    setAdvancedParams((prev) => ({
      ...prev,
      types: {
        ...prev.types,
        [typeSlug]: {
          ...prev.types?.[typeSlug],
          [fieldName]: value,
        },
      },
    }));
  };

  const handleFrameworkChange = (frameworkSlug: string, fieldName: string, value: string) => {
    setAdvancedParams((prev) => ({
      ...prev,
      framework: {
        [frameworkSlug]: {
          ...prev.framework?.[frameworkSlug],
          [fieldName]: value,
        },
      },
    }));
  };

  const activeTypeOptions = selectedTypes.map(slug => ({ slug, fields: advancedTypeOptions[slug as keyof typeof advancedTypeOptions] })).filter(opt => opt.fields?.length > 0);
  const activeFrameworkOptions = selectedFramework ? { slug: selectedFramework, fields: advancedFrameworkOptions[selectedFramework as keyof typeof advancedFrameworkOptions] } : null;

  return (
    <div className="my-6 p-4 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800/50">
      <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-4">Expert Configuration</h3>
      <div className="space-y-6">
        {activeTypeOptions.map(({ slug, fields }) => (
          <div key={slug} className="p-4 border border-gray-200 dark:border-gray-700 rounded-md bg-white dark:bg-gray-800">
            <h4 className="font-semibold text-gray-700 dark:text-gray-200 mb-2 capitalize">{slug.replace(/_/g, ' ')} Options</h4>
            <div className="space-y-3">
              {fields.map(field => (
                <div key={field.name}>
                  <label htmlFor={field.name} className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">{field.label}</label>
                  {renderField(field, advancedParams.types?.[slug]?.[field.name] || '', (e) => handleTypeChange(slug, field.name, e.target.value))}
                </div>
              ))}
            </div>
          </div>
        ))}

        {activeFrameworkOptions && activeFrameworkOptions.fields && (
          <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-md bg-white dark:bg-gray-800">
            <h4 className="font-semibold text-gray-700 dark:text-gray-200 mb-2 capitalize">{activeFrameworkOptions.slug.replace(/_/g, ' ')} Framework Options</h4>
            <div className="space-y-3">
              {activeFrameworkOptions.fields.map(field => (
                <div key={field.name}>
                  <label htmlFor={field.name} className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">{field.label}</label>
                  {renderField(field, advancedParams.framework?.[activeFrameworkOptions.slug]?.[field.name] || '', (e) => handleFrameworkChange(activeFrameworkOptions.slug, field.name, e.target.value))}
                </div>
              ))}
            </div>
          </div>
        )}

        {(activeTypeOptions.length === 0 && !activeFrameworkOptions?.fields) && (
            <p className="text-sm text-gray-500 dark:text-gray-400 text-center py-4">Select a Type or Framework with advanced options to configure them here.</p>
        )}
      </div>
    </div>
  );
};