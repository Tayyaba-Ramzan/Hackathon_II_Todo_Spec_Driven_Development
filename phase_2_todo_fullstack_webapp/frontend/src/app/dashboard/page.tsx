'use client';

import { useEffect, useState } from 'react';
import { getCurrentSession, logout } from '@/lib/session-utils';
import { Header } from '@/components/layout/Header';
import { taskApi, Task } from '@/lib/api';

const DashboardPage = () => {
  const [user, setUser] = useState<{ id: string; email: string } | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  // Load tasks from the backend API
  useEffect(() => {
    const loadTasks = async () => {
      if (user) {
        try {
          const tasksFromApi = await taskApi.getTasks();
          setTasks(tasksFromApi);
        } catch (error) {
          console.error('Error loading tasks from API:', error);
          setTasks([]);
        }
      }
    };

    // Load tasks initially
    loadTasks();

    // Set up event listener to reload tasks when localStorage changes
    // (for cross-tab synchronization)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'tasks' || e.key === 'auth-token') {
        loadTasks();
      }
    };

    window.addEventListener('storage', handleStorageChange);

    // Also reload tasks when the page becomes visible again
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        loadTasks();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    // Also reload tasks when the window is focused (in case of tab switching)
    const handleFocus = () => {
      loadTasks();
    };

    window.addEventListener('focus', handleFocus);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('focus', handleFocus);
    };
  }, [user]);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const session = await getCurrentSession();
        if (session) {
          setUser({ id: session.user.id, email: session.user.email });
        } else {
          // Redirect to login if not authenticated
          window.location.href = '/login';
        }
      } catch (error) {
        console.error('Error checking authentication:', error);
        // Redirect to login on error
        window.location.href = '/login';
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogout = async () => {
    try {
      // Call the logout API endpoint
      const response = await fetch('/api/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          request: 'signOut' // Specify this is a sign-out request
        })
      });

      if (response.ok) {
        // Clear the token and redirect
        await logout();
      } else {
        console.error('Logout API call failed');
        // Still clear the token and redirect even if API fails
        await logout();
      }
    } catch (error) {
      console.error('Error during logout:', error);
      // Clear the token and redirect even if API fails
      await logout();
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-cyan-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
        <div className="text-xl text-gray-700 dark:text-gray-300 flex flex-col items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
          <span>Loading your dashboard...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      <Header user={user} onLogout={handleLogout} />

      <main className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="mb-16 text-center relative">
  {/* Floating neon accent behind hero */}
  <div className="absolute -z-10 top-0 left-1/2 transform -translate-x-1/2 w-[500px] h-[500px] bg-gradient-to-tr from-purple-500 via-indigo-500 to-pink-500 rounded-full opacity-20 blur-3xl animate-blob"></div>

  <h1 className="text-5xl md:text-6xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-700 via-purple-600 to-pink-500 mb-6 animate-text-flicker">
    Hey, {user?.email.split('@')[0]} 
  </h1>

  <p className="text-lg md:text-xl text-gray-700 dark:text-gray-300 max-w-3xl mx-auto mb-8">
    🚀 Supercharge your productivity. Track your tasks, stay ahead, and turn your ideas into results—effortlessly.
  </p>

  <div className="inline-flex rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 p-1 shadow-xl hover:shadow-2xl transition-all">
    <a
      href="/tasks"
      className="inline-flex items-center justify-center rounded-full bg-white dark:bg-gray-900 px-8 py-4 text-lg font-semibold text-indigo-700 dark:text-white hover:scale-105 transition-transform shadow-md hover:shadow-lg"
    >
      Start a New Task
      <svg xmlns="http://www.w3.org/2000/svg" className="ml-3 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
      </svg>
    </a>
  </div>

  {/* Extra animations */}
  <style jsx>{`
    @keyframes blob {
      0%,100% { transform: translate(0,0) scale(1); }
      33% { transform: translate(30px,-50px) scale(1.1); }
      66% { transform: translate(-20px,20px) scale(0.9); }
    }
    .animate-blob { animation: blob 8s infinite; }
    @keyframes text-flicker {
      0%,100% { opacity: 1; }
      50% { opacity: 0.87; }
    }
    .animate-text-flicker { animation: text-flicker 2s infinite; }
  `}</style>
</div>


        {/* Stats Cards */}
       <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
  {/* Total Tasks */}
  <div className="relative bg-white/80 dark:bg-gray-900/80 backdrop-blur-md rounded-3xl border border-gray-200 dark:border-gray-800 p-6 shadow-xl hover:shadow-2xl transform transition-all duration-500 hover:scale-105">
    <div className="flex items-center">
      <div className="rounded-lg bg-gradient-to-tr from-indigo-400 to-indigo-600 p-4 text-white shadow-lg flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      </div>
      <div className="ml-5">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Total Tasks</h3>
        <p className="text-4xl font-extrabold text-indigo-700 dark:text-indigo-400">{tasks.length}</p>
      </div>
    </div>
  </div>

  {/* Completed Tasks */}
  <div className="relative bg-white/80 dark:bg-gray-900/80 backdrop-blur-md rounded-3xl border border-gray-200 dark:border-gray-800 p-6 shadow-xl hover:shadow-2xl transform transition-all duration-500 hover:scale-105">
    <div className="flex items-center">
      <div className="rounded-lg bg-gradient-to-tr from-green-400 to-green-600 p-4 text-white shadow-lg flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div className="ml-5">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Completed</h3>
        <p className="text-4xl font-extrabold text-green-600 dark:text-green-400">
          {tasks.filter(task => task.completed).length}
        </p>
      </div>
    </div>
  </div>

  {/* Pending Tasks */}
  <div className="relative bg-white/80 dark:bg-gray-900/80 backdrop-blur-md rounded-3xl border border-gray-200 dark:border-gray-800 p-6 shadow-xl hover:shadow-2xl transform transition-all duration-500 hover:scale-105">
    <div className="flex items-center">
      <div className="rounded-lg bg-gradient-to-tr from-amber-400 to-amber-600 p-4 text-white shadow-lg flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div className="ml-5">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Pending</h3>
        <p className="text-4xl font-extrabold text-amber-600 dark:text-amber-400">
          {tasks.filter(task => !task.completed).length}
        </p>
      </div>
    </div>
  </div>
</div>


        {/* Recent Tasks Preview */}
        {tasks.length > 0 && (
  <div className="mb-16">
    <div className="flex items-center justify-between mb-8">
      <h2 className="text-3xl font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent dark:from-indigo-400 dark:to-purple-400">
        Latest Tasks
      </h2>
      <a
        href="/tasks"
        className="text-indigo-600 dark:text-indigo-400 font-semibold hover:underline transition-colors"
      >
        View All
      </a>
    </div>

    <div className="space-y-4">
      {tasks.slice(0, 5).map((task) => (
        <div
          key={task.id}
          className={`relative p-5 rounded-3xl border ${
            task.completed
              ? 'bg-green-50/70 dark:bg-green-900/20 border-green-300 dark:border-green-700'
              : 'bg-gray-50/70 dark:bg-gray-900/20 border-gray-200 dark:border-gray-700'
          } shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-500 backdrop-blur-md`}
        >
          <div className="flex items-start">
            {/* Task Status */}
            <div
              className={`flex-shrink-0 w-6 h-6 mt-1 rounded-full border flex items-center justify-center ${
                task.completed
                  ? 'bg-green-500 border-green-500'
                  : 'border-gray-300 dark:border-gray-600'
              }`}
            >
              {task.completed && (
                <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                </svg>
              )}
            </div>

            {/* Task Info */}
            <div className="ml-4 flex-1">
              <h3
                className={`text-lg font-semibold ${
                  task.completed
                    ? 'text-green-800 dark:text-green-200 line-through'
                    : 'text-gray-900 dark:text-gray-100'
                }`}
              >
                {task.title}
              </h3>

              {task.description && (
                <p className="mt-1 text-sm text-gray-600 dark:text-gray-400 line-clamp-1">
                  {task.description}
                </p>
              )}

              {/* Dates */}
              <div className="mt-2 flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
                <span className="flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {task.createdAt ? new Date(task.createdAt).toLocaleDateString('en-US') : 'Unknown'}
                </span>

                {task.completed && task.updatedAt && (
                  <span className="flex items-center gap-1 text-green-600 dark:text-green-400">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Completed: {task.updatedAt ? new Date(task.updatedAt).toLocaleDateString('en-US') : 'Unknown'}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
)}


        {/* Quick Actions */}
        <div className="bg-white dark:bg-gray-900 rounded-3xl border border-gray-200 dark:border-gray-800 p-8 shadow-xl">
  {/* Header */}
  <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-10">
    <div>
      <h2 className="text-3xl font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent dark:from-indigo-400 dark:to-purple-400 mb-1">
        Quick Actions
      </h2>
      <p className="text-gray-600 dark:text-gray-400 font-medium">
        Take control of your tasks instantly
      </p>
    </div>
    <a
      href="/tasks"
      className="mt-4 md:mt-0 inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 px-7 py-3 text-base font-semibold text-white shadow-lg transition-all hover:scale-105 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
    >
      Manage All Tasks
      <svg xmlns="http://www.w3.org/2000/svg" className="ml-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
      </svg>
    </a>
  </div>

  {/* Action Cards */}
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    {/* View All Tasks */}
    <div className="p-6 bg-white/60 dark:bg-gray-900/30 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-md backdrop-blur-md hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-500">
      <div className="flex items-center mb-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 text-indigo-600 dark:text-indigo-400">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 className="ml-4 text-lg font-semibold text-gray-900 dark:text-white">View All Tasks</h3>
      </div>
      <p className="text-gray-600 dark:text-gray-400 mb-4">
        See all your tasks in one place with a smooth, modern interface.
      </p>
      <a
        href="/tasks"
        className="inline-flex items-center text-indigo-600 hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 font-semibold transition-colors"
      >
        Go to tasks
        <svg xmlns="http://www.w3.org/2000/svg" className="ml-1 h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </a>
    </div>

    {/* Create New Task */}
    <div className="p-6 bg-white/60 dark:bg-gray-900/30 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-md backdrop-blur-md hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-500">
      <div className="flex items-center mb-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-tr from-green-100 to-emerald-100 dark:from-green-900/30 dark:to-emerald-900/30 text-green-600 dark:text-green-400">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </div>
        <h3 className="ml-4 text-lg font-semibold text-gray-900 dark:text-white">Create New Task</h3>
      </div>
      <p className="text-gray-600 dark:text-gray-400 mb-4">
        Add a new task quickly and stay ahead of your productivity goals.
      </p>
      <a
        href="/tasks"
        className="inline-flex items-center text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-300 font-semibold transition-colors"
      >
        Create task
        <svg xmlns="http://www.w3.org/2000/svg" className="ml-1 h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </a>
    </div>
  </div>
</div>

      </main>
    </div>
  );
};

export default DashboardPage;