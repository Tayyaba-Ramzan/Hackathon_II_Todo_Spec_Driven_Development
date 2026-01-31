// Define the Task type
interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
  userId: string;
}

// Extend the global type to include our tasks property
declare global {
  var tasks: Task[];
}

// Global in-memory storage for tasks
// In a real application, this would be a database
if (!global.tasks) {
  global.tasks = [];
  // Load tasks from localStorage if available
  if (typeof window !== 'undefined' && window.localStorage) {
    const storedTasks = localStorage.getItem('tasks');
    if (storedTasks) {
      try {
        global.tasks = JSON.parse(storedTasks);
      } catch (error) {
        console.error('Error parsing tasks from localStorage:', error);
        global.tasks = [];
      }
    }
  }
}

// Export the tasks array as the storage interface
export const taskStorage = {
  get tasks() {
    return global.tasks;
  },
  setTasks(tasks: Task[]) {
    global.tasks = tasks;
    // Persist to localStorage if available
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem('tasks', JSON.stringify(tasks));
    }
  },
  addTask(task: Task) {
    global.tasks.push(task);
    // Persist to localStorage if available
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem('tasks', JSON.stringify(global.tasks));
    }
  },
  updateTask(id: string, updatedTask: Partial<Task>) {
    const index = global.tasks.findIndex(task => task.id === id);
    if (index !== -1) {
      global.tasks[index] = { ...global.tasks[index], ...updatedTask };
      // Persist to localStorage if available
      if (typeof window !== 'undefined' && window.localStorage) {
        localStorage.setItem('tasks', JSON.stringify(global.tasks));
      }
    }
  },
  deleteTask(id: string) {
    global.tasks = global.tasks.filter(task => task.id !== id);
    // Persist to localStorage if available
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem('tasks', JSON.stringify(global.tasks));
    }
  }
};