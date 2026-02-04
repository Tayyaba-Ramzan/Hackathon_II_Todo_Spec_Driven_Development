import React, { useState } from 'react';
import { Task } from '@/lib/api';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onToggleComplete,
  onEdit,
  onDelete
}) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={`
        relative rounded-2xl border bg-white shadow-lg transition-all duration-300 ease-in-out
        ${isHovered ? 'shadow-xl -translate-y-1 border-indigo-200 dark:border-indigo-900/50' : 'border-gray-200/70 dark:border-gray-800'}
        ${task.completed ? 'opacity-90 dark:opacity-80 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800/50 dark:to-gray-900/50' : 'bg-gradient-to-br from-white to-gray-50 dark:from-gray-900 dark:to-gray-900/80'}
        overflow-hidden
      `}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="p-6">
        <div className="flex items-start space-x-4">
          <button
            onClick={(e) => {
              e.stopPropagation(); // Prevent event bubbling
              onToggleComplete(task);
            }}
            className={`
              flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full border-2 transition-all duration-200
              ${task.completed
                ? 'bg-gradient-to-r from-indigo-500 to-purple-600 border-indigo-500 shadow-inner'
                : 'border-gray-300 bg-white hover:border-indigo-400 dark:border-gray-700 dark:bg-gray-800 dark:hover:border-indigo-500'
              }
            `}
            aria-label={task.completed ? "Mark task as incomplete" : "Mark task as complete"}
          >
            {task.completed && (
              <svg
                className="h-4 w-4 text-white"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="3"
              >
                <path d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>
          <div className="flex-1 min-w-0">
            <h3 className={`
              text-lg font-semibold transition-colors
              ${task.completed
                ? 'line-through text-gray-500 dark:text-gray-400'
                : 'text-gray-900 dark:text-gray-100 hover:text-indigo-600 dark:hover:text-indigo-400'}
            `}>
              {task.title}
            </h3>
            {task.description && (
              <p className="mt-3 text-gray-600 dark:text-gray-400">
                {task.description}
              </p>
            )}
            <div className="mt-4 flex items-center text-sm text-gray-500 dark:text-gray-500">
              <span className="inline-flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="mr-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Created: {task.createdAt ? new Date(task.createdAt).toLocaleDateString('en-US') : 'Date unknown'}
              </span>
              {task.completed && task.updatedAt && (
                <span className="ml-4 inline-flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="mr-1 h-4 w-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Completed: {task.updatedAt ? new Date(task.updatedAt).toLocaleDateString('en-US') : 'Date unknown'}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className={`
        absolute right-5 top-5 flex space-x-2
        ${isHovered ? 'opacity-100' : 'opacity-0'}
        transition-opacity duration-300
      `}>
        <button
          onClick={() => onEdit(task)}
          className="rounded-lg p-2 text-gray-500 hover:bg-indigo-100 hover:text-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-indigo-400 transition-colors shadow-sm"
          aria-label="Edit task"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
          </svg>
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="rounded-lg p-2 text-gray-500 hover:bg-red-100 hover:text-red-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-red-400 transition-colors shadow-sm"
          aria-label="Delete task"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export { TaskCard };