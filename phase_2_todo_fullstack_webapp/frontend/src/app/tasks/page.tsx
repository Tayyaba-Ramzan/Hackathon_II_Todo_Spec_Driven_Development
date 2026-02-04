'use client';

import { useState, useEffect } from 'react';
import { TaskCard } from '@/components/tasks/TaskCard';
import { TaskForm } from '@/components/tasks/TaskForm';
import { getCurrentSession, logout } from '@/lib/session-utils';
import { Header } from '@/components/layout/Header';
import { taskApi, Task, CreateTaskData, UpdateTaskData } from '@/lib/api';

const TasksPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [user, setUser] = useState<{ id: string; email: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState<string | null>(null);

  // Check authentication and load tasks on component mount
  useEffect(() => {
    let isMounted = true; // Flag to track if component is still mounted

    const loadTasks = async () => {
      try {
        const session = await getCurrentSession();
        if (session && isMounted) {
          setUser({ id: session.user.id, email: session.user.email });

          // Load tasks from the backend API
          const tasksFromApi = await taskApi.getTasks();
          if (isMounted) {
            setTasks(tasksFromApi);
          }
        } else if (isMounted) {
          // Redirect to login if not authenticated
          window.location.href = '/login';
          return; // Exit early to prevent setting loading to false
        }
      } catch (error) {
        console.error('Error loading tasks:', error);
        if (isMounted) {
          setError(error instanceof Error ? error.message : 'Failed to load tasks');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadTasks();

    // Cleanup function to set isMounted to false when component unmounts
    return () => {
      isMounted = false;
    };
  }, []); // Empty dependency array to run only once on mount

  // Handle adding a new task
  const handleAddTask = async (taskData: { title: string; description: string }) => {
    try {
      setError(null);
      const newTaskData: CreateTaskData = {
        title: taskData.title,
        description: taskData.description,
        completed: false
      };

      const newTask = await taskApi.createTask(newTaskData);
      setTasks(prevTasks => [newTask, ...prevTasks]);
      setEditingTask(null);
    } catch (error) {
      console.error('Error adding task:', error);
      setError(error instanceof Error ? error.message : 'Failed to add task');
    }
  };

  // Handle updating a task
  const handleUpdateTask = async (taskData: { title: string; description: string }) => {
    if (!editingTask) return;

    try {
      setError(null);
      const updateData: UpdateTaskData = {
        title: taskData.title,
        description: taskData.description
      };

      const updatedTask = await taskApi.updateTask(editingTask.id, updateData);
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === editingTask.id ? updatedTask : task
        )
      );
      setEditingTask(null);
    } catch (error) {
      console.error('Error updating task:', error);
      setError(error instanceof Error ? error.message : 'Failed to update task');
    }
  };

  // Handle toggling task completion
  const handleToggleComplete = async (task: Task) => {
    try {
      setError(null);
      const updatedTask = await taskApi.patchTask(task.id, {
        completed: !task.completed
      });

      setTasks(prevTasks =>
        prevTasks.map(t =>
          t.id === task.id ? updatedTask : t
        )
      );
    } catch (error) {
      console.error('Error toggling task completion:', error);
      setError(error instanceof Error ? error.message : 'Failed to update task');
    }
  };

  // Handle editing a task
  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  // Handle deleting a task
  const handleDeleteTask = async (id: string) => {
    try {
      setError(null);
      await taskApi.deleteTask(id);
      setTasks(prevTasks => prevTasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
      setError(error instanceof Error ? error.message : 'Failed to delete task');
    }
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  const handleLogout = async () => {
    try {
      // Clear the token and redirect
      await logout();
    } catch (error) {
      console.error('Error during logout:', error);
      // Still clear the token and redirect even if API fails
      await logout();
    }
  };

  // Filter and search tasks based on selected filter and search query
  const filteredTasks = tasks.filter(task => {
    // Apply filter
    let passesFilter = true;
    if (filter === 'active') passesFilter = !task.completed;
    if (filter === 'completed') passesFilter = task.completed;

    // Apply search
    const matchesSearch =
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.description.toLowerCase().includes(searchQuery.toLowerCase());

    return passesFilter && matchesSearch;
  });

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-cyan-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
        <div className="text-xl text-gray-700 dark:text-gray-300 flex flex-col items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
          <span>Loading your tasks...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      <Header user={user} onLogout={handleLogout} />

      <main className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 dark:bg-red-900/20 dark:border-red-800 dark:text-red-300 shadow-sm">
            {error}
          </div>
        )}

        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Tasks</h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} in total
              </p>
            </div>

            <div className="mt-4 md:mt-0 flex space-x-1 bg-gray-100 dark:bg-gray-800 rounded-xl p-1">
              <button
                onClick={() => setFilter('all')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filter === 'all'
                    ? 'bg-white text-indigo-600 shadow-sm dark:bg-gray-700'
                    : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setFilter('active')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filter === 'active'
                    ? 'bg-white text-indigo-600 shadow-sm dark:bg-gray-700'
                    : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                Active
              </button>
              <button
                onClick={() => setFilter('completed')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filter === 'completed'
                    ? 'bg-white text-indigo-600 shadow-sm dark:bg-gray-700'
                    : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                Completed
              </button>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6 shadow-lg mb-6 transition-all duration-300 hover:shadow-xl">
            <TaskForm
              onSubmit={editingTask ? handleUpdateTask : handleAddTask}
              onCancel={editingTask ? handleCancelEdit : undefined}
              initialData={editingTask || null}
            />
          </div>

          <div className="relative mb-6">
            <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 rounded-xl border border-gray-300 bg-white text-base focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white transition-all duration-200"
            />
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            {filter === 'all' && 'All Tasks'}
            {filter === 'active' && 'Active Tasks'}
            {filter === 'completed' && 'Completed Tasks'}
          </h2>

          {filteredTasks.length === 0 ? (
            <div className="text-center py-16">
              <div className="mx-auto h-24 w-24 flex items-center justify-center rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-indigo-500 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                {filter === 'completed' ? 'No completed tasks yet' :
                 filter === 'active' ? 'No active tasks' : 'No tasks yet'}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md mx-auto">
                {filter === 'completed' ? 'Complete some tasks to see them here' :
                 filter === 'active' ? 'All your tasks are completed! Add a new one.' :
                 'Get started by adding a new task using the form above.'}
              </p>
              {filter === 'completed' && (
                <button
                  onClick={() => setFilter('active')}
                  className="inline-flex items-center rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 px-4 py-2 text-sm font-medium text-white shadow-lg transition-all hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
                >
                  View Active Tasks
                </button>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredTasks.map(task => (
                <div key={task.id} className="transition-all duration-300 hover:scale-[1.02]">
                  <TaskCard
                    task={task}
                    onToggleComplete={handleToggleComplete}
                    onEdit={handleEditTask}
                    onDelete={handleDeleteTask}
                  />
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default TasksPage;