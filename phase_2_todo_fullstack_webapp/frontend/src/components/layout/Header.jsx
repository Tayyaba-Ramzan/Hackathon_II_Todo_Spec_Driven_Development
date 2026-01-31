import React from 'react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/ui/ThemeToggle';

const Header = ({ user, onLogout }) => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200/20 bg-white/80 backdrop-blur-md dark:border-gray-800/30 dark:bg-gray-900/80 shadow-sm">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo & Navigation */}
          <div className="flex items-center space-x-6">
            <Link href="/dashboard" className="flex items-center space-x-2 group">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-tr from-indigo-600 to-purple-600 text-white shadow-md transition-transform transform group-hover:scale-110">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <span className="text-2xl font-extrabold text-gray-900 dark:text-white tracking-tight">
                TodoPro
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              <Link
                href="/dashboard"
                className="text-sm font-semibold text-gray-700 hover:text-indigo-600 dark:text-gray-300 dark:hover:text-indigo-400 transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/tasks"
                className="text-sm font-semibold text-gray-700 hover:text-indigo-600 dark:text-gray-300 dark:hover:text-indigo-400 transition-colors"
              >
                My Tasks
              </Link>
              <Link
                href="/analytics"
                className="text-sm font-semibold text-gray-700 hover:text-indigo-600 dark:text-gray-300 dark:hover:text-indigo-400 transition-colors"
              >
                Analytics
              </Link>
            </nav>
          </div>

          {/* Right Side: Theme & User */}
          <div className="flex items-center space-x-4">
            <ThemeToggle />

            {user && (
              <div className="flex items-center space-x-3">
                <span className="hidden md:block text-sm font-medium text-gray-600 dark:text-gray-400">
                  {user.email}
                </span>
                <button
                  onClick={onLogout}
                  className="rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 px-4 py-2 text-sm font-semibold text-white shadow-md transition-all hover:from-indigo-700 hover:to-purple-700 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
                >
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export { Header };
