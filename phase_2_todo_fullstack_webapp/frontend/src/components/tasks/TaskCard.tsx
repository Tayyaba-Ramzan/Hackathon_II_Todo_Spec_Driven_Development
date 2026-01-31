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
        relative rounded-3xl border backdrop-blur-lg bg-white/40 dark:bg-gray-900/50 shadow-lg transition-all duration-300 ease-in-out
        ${isHovered ? 'shadow-2xl -translate-y-1 border-indigo-300 dark:border-indigo-800' : 'border-gray-200/30 dark:border-gray-700/50'}
        ${task.completed ? 'opacity-90' : 'opacity-100'}
        overflow-hidden
      `}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Overlay gradient hover */}
      <div className={`
        absolute inset-0 rounded-3xl pointer-events-none transition-all duration-500
        ${isHovered ? 'bg-gradient-to-br from-indigo-100/20 via-purple-100/20 to-pink-100/20 dark:from-indigo-800/20 dark:via-purple-800/20 dark:to-pink-800/20' : ''}
      `}></div>

      <div className="relative p-6 space-y-4">
        <div className="flex items-start space-x-4">
          
          {/* Complete Button */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              onToggleComplete(task);
            }}
            className={`
              flex h-7 w-7 items-center justify-center rounded-full border-2 transition-all duration-200
              ${task.completed
                ? 'bg-gradient-to-r from-indigo-500 to-purple-600 border-indigo-500 shadow-inner text-white'
                : 'border-gray-300 bg-white hover:border-indigo-400 dark:border-gray-600 dark:bg-gray-800 dark:hover:border-indigo-500'
              }
            `}
            aria-label={task.completed ? "Mark task as incomplete" : "Mark task as complete"}
          >
            {task.completed && (
              <svg
                className="h-4 w-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="3"
              >
                <path d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>

          {/* Task Info */}
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
              <p className="mt-2 text-gray-600 dark:text-gray-300 line-clamp-3">
                {task.description}
              </p>
            )}
            <div className="mt-3 flex flex-wrap items-center text-sm text-gray-500 dark:text-gray-400 gap-3">
              <span className="inline-flex items-center space-x-1">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {task.createdAt ? new Date(task.createdAt).toLocaleDateString('en-US') : 'Unknown'}
              </span>
              {task.completed && task.updatedAt && (
                <span className="inline-flex items-center space-x-1 text-green-500">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {task.updatedAt ? new Date(task.updatedAt).toLocaleDateString('en-US') : 'Unknown'}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Edit / Delete Actions */}
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
          className="rounded-lg p-2 text-gray-500 hover:bg-red-100 hover:text-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-red-400 transition-colors shadow-sm"
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
