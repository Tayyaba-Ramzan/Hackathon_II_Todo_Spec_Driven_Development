import React from 'react';
import { useResponsive } from '@/hooks/useResponsive';

interface ResponsiveGridProps {
  children: React.ReactNode;
  minColumnWidth?: string;
  gap?: string;
  className?: string;
}

const ResponsiveGrid: React.FC<ResponsiveGridProps> = ({
  children,
  minColumnWidth = '20rem',
  gap = 'gap-6',
  className = ''
}) => {
  const { isMobile, isTablet, isDesktop } = useResponsive();

  // Determine grid columns based on screen size
  let gridColsClass = 'grid-cols-1'; // Default for mobile

  if (isTablet) {
    gridColsClass = 'grid-cols-2'; // Tablet
  }

  if (isDesktop) {
    gridColsClass = 'grid-cols-3'; // Desktop
  }

  return (
    <div
      className={`grid ${gridColsClass} ${gap} ${className}`}
      style={{
        gridTemplateColumns: isDesktop ? `repeat(auto-fit, minmax(${minColumnWidth}, 1fr))` : undefined
      }}
    >
      {children}
    </div>
  );
};

export { ResponsiveGrid };