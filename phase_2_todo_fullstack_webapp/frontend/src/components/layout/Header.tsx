'use client';

import React from 'react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/ui/ThemeToggle';

interface User {
  id: string;
  email: string;
}

interface HeaderProps {
  user: User | null;
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ user, onLogout }) => {
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
              <span className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent dark:from-indigo-400 dark:to-purple-400">
                TaskMate
              </span>
            </Link>

            {/* Desktop Nav */}
            <nav className="hidden md:flex space-x-3">
              <Link
                href="/dashboard"
                className="rounded-lg px-4 py-2 text-sm font-semibold text-gray-700 hover:text-indigo-600 hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:text-gray-300 dark:hover:text-indigo-400 dark:hover:bg-gray-800"
              >
                Dashboard
              </Link>
              <Link
                href="/tasks"
                className="rounded-lg px-4 py-2 text-sm font-semibold text-gray-700 hover:text-indigo-600 hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:text-gray-300 dark:hover:text-indigo-400 dark:hover:bg-gray-800"
              >
                My Tasks
              </Link>
            </nav>
          </div>

          {/* Right Side: Theme & User */}
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            {user && (
              <div className="flex items-center space-x-3">
                <span className="hidden md:block truncate text-sm font-medium text-gray-600 dark:text-gray-300 max-w-[140px]">
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
