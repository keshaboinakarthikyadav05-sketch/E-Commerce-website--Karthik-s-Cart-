import React from 'react';

export const SkeletonCard: React.FC = () => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 p-4 animate-pulse flex flex-col justify-between">
      <div>
        <div className="aspect-square bg-slate-200 rounded-xl mb-3" />
        <div className="h-3 bg-slate-200 rounded w-1/3 mb-2" />
        <div className="h-4 bg-slate-200 rounded w-4/5 mb-1.5" />
        <div className="h-4 bg-slate-200 rounded w-2/3 mb-3" />
        <div className="h-3 bg-slate-200 rounded w-1/4 mb-4" />
      </div>
      <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
        <div className="h-5 bg-slate-200 rounded w-1/3" />
        <div className="h-8 bg-slate-200 rounded-xl w-16" />
      </div>
    </div>
  );
};
