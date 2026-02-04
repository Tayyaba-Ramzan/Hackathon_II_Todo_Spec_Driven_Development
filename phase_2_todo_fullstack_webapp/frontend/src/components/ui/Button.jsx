import React from 'react';
import { cva } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background',
  {
    variants: {
      variant: {
        default: 'bg-indigo-600 text-white hover:bg-indigo-700',
        destructive: 'bg-red-500 text-white hover:bg-red-600',
        outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-50 hover:bg-gray-200 dark:hover:bg-gray-700',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'underline-offset-4 hover:underline text-indigo-600 dark:text-indigo-400',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-9 px-3 rounded-md',
        lg: 'h-11 px-8 rounded-md',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

// Define the props type using JSDoc for type checking
/**
 * @typedef {Object} ButtonProps
 * @property {string} [variant] - The variant of the button
 * @property {string} [size] - The size of the button
 * @property {string} [className] - Additional CSS classes
 * @property {boolean} [asChild] - Whether to render as child
 * @property {React.HTMLAttributes<HTMLButtonElement>['type']} [type] - The type of button
 * @property {React.HTMLAttributes<HTMLButtonElement>['disabled']} [disabled] - Whether the button is disabled
 * @property {React.Ref<HTMLButtonElement>} [ref] - Ref for the button element
 */

const Button = React.forwardRef(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };