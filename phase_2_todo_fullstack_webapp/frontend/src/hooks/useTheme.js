import { useState, useEffect } from 'react';

export function useTheme() {
  const [theme, setThemeState] = useState('system');

  useEffect(() => {
    // Initialize theme from localStorage or system preference
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme && ['light', 'dark', 'system'].includes(storedTheme)) {
      setThemeState(storedTheme);
    } else {
      // Default to system preference
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setThemeState(systemPrefersDark ? 'dark' : 'light');
    }
  }, []);

  const setTheme = (newTheme) => {
    setThemeState(newTheme);
    localStorage.setItem('theme', newTheme);

    // Apply theme class to document element
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');

    let actualTheme = newTheme;
    if (newTheme === 'system') {
      actualTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
    }

    root.classList.add(actualTheme);
  };

  // Apply theme when theme state changes
  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');

    let actualTheme = theme;
    if (theme === 'system') {
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      actualTheme = systemPrefersDark ? 'dark' : 'light';
    }

    root.classList.add(actualTheme);
  }, [theme]);

  return { theme, setTheme };
}