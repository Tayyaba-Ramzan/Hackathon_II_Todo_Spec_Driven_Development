import React from 'react';

const Checkbox = ({ checked, onChange, className = '', ...props }) => {
  return (
    <input
      type="checkbox"
      checked={checked}
      onChange={onChange}
      className={`h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:ring-offset-gray-800 ${className}`}
      {...props}
    />
  );
};

export { Checkbox };