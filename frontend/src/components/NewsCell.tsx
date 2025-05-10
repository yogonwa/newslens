import React, { useState } from 'react';
import { NewsSnapshot, NewsSource } from '../types';

interface NewsCellProps {
  snapshot: NewsSnapshot;
  source: NewsSource;
  onClick: () => void;
}

const NewsCell: React.FC<NewsCellProps> = ({ snapshot, source, onClick }) => {
  const [isHovered, setIsHovered] = useState(false);
  
  // Calculate sentiment color
  const getSentimentColor = (score: number) => {
    if (score <= -0.5) return 'bg-red-500';
    if (score < 0) return 'bg-orange-500';
    if (score === 0) return 'bg-gray-500';
    if (score <= 0.5) return 'bg-green-400';
    return 'bg-green-600';
  };

  // Calculate magnitude width
  const getMagnitudeWidth = (magnitude: number) => {
    return `${magnitude * 100}%`;
  };

  return (
    <div 
      className="relative rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02] cursor-pointer w-full h-full bg-gray-100"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={onClick}
    >
      {/* Source badge */}
      <div 
        className="absolute top-2 left-2 z-10 px-2 py-1 rounded text-xs font-bold text-white"
        style={{ backgroundColor: source.color }}
      >
        {source.name}
      </div>
      
      {/* Thumbnail */}
      <img 
        src={snapshot.thumbnailUrl} 
        alt={`${source.name} homepage`}
        className="w-full h-full object-cover transition-opacity duration-300"
        style={{ opacity: isHovered ? 0.3 : 1 }}
      />
      
      {/* Hover overlay with headline */}
      <div 
        className={`absolute inset-0 p-4 flex flex-col justify-center bg-black bg-opacity-70 transition-opacity duration-300 ${
          isHovered ? 'opacity-100' : 'opacity-0'
        }`}
      >
        <h3 className="text-white text-lg font-bold mb-2">{snapshot.mainHeadline}</h3>
        {snapshot.subHeadlines.map((headline, index) => (
          <p key={index} className="text-gray-200 text-sm">{headline}</p>
        ))}
        
        {/* Sentiment indicator */}
        <div className="mt-auto">
          <div className="flex items-center justify-between text-xs text-white mb-1">
            <span>Sentiment</span>
            <span>{snapshot.sentiment.score.toFixed(1)}</span>
          </div>
          <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
            <div 
              className={`h-full ${getSentimentColor(snapshot.sentiment.score)}`}
              style={{ width: getMagnitudeWidth(snapshot.sentiment.magnitude) }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewsCell;