import { useState, useEffect } from 'react';

export function useResponsive() {
  const [breakpoint, setBreakpoint] = useState('mobile');

  useEffect(() => {
    const updateBreakpoint = () => {
      const width = window.innerWidth;
      
      if (width >= 1024) {
        setBreakpoint('desktop');
      } else if (width >= 640) {
        setBreakpoint('tablet');
      } else {
        setBreakpoint('mobile');
      }
    };

    // Initial check
    updateBreakpoint();

    // Add resize listener
    window.addEventListener('resize', updateBreakpoint);

    // Cleanup listener on unmount
    return () => window.removeEventListener('resize', updateBreakpoint);
  }, []);

  return {
    breakpoint,
    isMobile: breakpoint === 'mobile',
    isTablet: breakpoint === 'tablet',
    isDesktop: breakpoint === 'desktop',
  };
}