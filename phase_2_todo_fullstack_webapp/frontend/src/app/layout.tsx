import './globals.css';
import { ThemeProvider } from '@/contexts/ThemeContext';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Todo App | Productivity at Your Fingertips',
  description: 'A beautiful and modern todo application with secure authentication',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-gray-50 dark:bg-gray-950 antialiased">
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}