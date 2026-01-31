import React from 'react';

const Skeleton = ({ className = '', ...props }) => {
  return (
    <div
      className={`animate-pulse bg-gray-200 dark:bg-gray-700 rounded-md ${className}`}
      {...props}
    />
  );
};

const SkeletonLine = ({ width = '100%', height = '1rem', className = '' }) => {
  return (
    <Skeleton 
      className={`h-${height} w-${width} ${className}`} 
    />
  );
};

const SkeletonCircle = ({ size = '1rem', className = '' }) => {
  return (
    <Skeleton 
      className={`w-${size} h-${size} rounded-full ${className}`} 
    />
  );
};

const SkeletonRectangle = ({ width = '100%', height = '1rem', className = '' }) => {
  return (
    <Skeleton 
      className={`w-${width} h-${height} ${className}`} 
    />
  );
};

export { Skeleton, SkeletonLine, SkeletonCircle, SkeletonRectangle };