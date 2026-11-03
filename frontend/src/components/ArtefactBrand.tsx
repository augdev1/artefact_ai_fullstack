import React from 'react';

export const ArtefactLetterA: React.FC<{ className?: string }> = ({ className = 'w-6 h-6 inline-block text-white' }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="3.2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <polyline points="4 21 12 3 20 21" />
  </svg>
);

export const ArtefactBrand: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center select-none py-1">
      <div className="flex items-center tracking-[0.28em] font-extrabold text-xl md:text-2xl text-white font-display">
        <ArtefactLetterA className="w-5 h-5 md:w-6 md:h-6 mr-0.5 text-white" />
        <span>RTEF</span>
        <ArtefactLetterA className="w-5 h-5 md:w-6 md:h-6 mx-0.5 text-white" />
        <span>CT</span>
      </div>
      <div className="h-[2.5px] w-16 md:w-20 bg-gradient-to-r from-[#E60067] via-[#FF2D75] to-[#E60067] rounded-full mt-1"></div>
    </div>
  );
};

