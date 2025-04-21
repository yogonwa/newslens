import React from 'react';
import { NewsSnapshot, NewsSource } from '../types';
import { X, AlertTriangle, ThumbsUp, ChevronLeft, ChevronRight } from 'lucide-react';

interface NewsDetailProps {
  snapshot: NewsSnapshot;
  source: NewsSource;
  onClose: () => void;
  onPrevious?: () => void;
  onNext?: () => void;
  hasPrevious: boolean;
  hasNext: boolean;
}

const NewsDetail: React.FC<NewsDetailProps> = ({ 
  snapshot, 
  source, 
  onClose, 
  onPrevious, 
  onNext,
  hasPrevious,
  hasNext 
}) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      hour12: true
    });
  };

  // Sentiment analysis helpers
  const getSentimentLabel = (score: number) => {
    if (score <= -0.5) return 'Highly Negative';
    if (score < 0) return 'Negative';
    if (score < 0.1 && score > -0.1) return 'Neutral';
    if (score <= 0.5) return 'Positive';
    return 'Highly Positive';
  };

  const getSentimentIcon = (score: number) => {
    if (score < 0) return <AlertTriangle className="w-5 h-5 text-orange-500" />;
    return <ThumbsUp className="w-5 h-5 text-green-500" />;
  };

  const getSentimentColor = (score: number) => {
    if (score <= -0.5) return 'text-red-600';
    if (score < 0) return 'text-orange-500';
    if (score < 0.1 && score > -0.1) return 'text-gray-500';
    if (score <= 0.5) return 'text-green-500';
    return 'text-green-600';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-80 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] flex flex-col relative">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center">
            <div 
              className="w-8 h-8 rounded flex items-center justify-center mr-3 text-white font-bold text-xs"
              style={{ backgroundColor: source.color }}
            >
              {source.name.substring(0, 2).toUpperCase()}
            </div>
            <div>
              <h2 className="text-xl font-bold">{source.name}</h2>
              <p className="text-sm text-gray-500">{formatDate(snapshot.timestamp)}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              {getSentimentIcon(snapshot.sentiment.score)}
              <span className={`ml-1 ${getSentimentColor(snapshot.sentiment.score)}`}>
                {getSentimentLabel(snapshot.sentiment.score)}
              </span>
            </div>
            <button 
              onClick={onClose}
              className="rounded-full p-1 hover:bg-gray-200 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>
        
        {/* Content */}
        <div className="flex-1 overflow-auto p-4">
          <div className="bg-gray-100 p-4 rounded-lg mb-4">
            <h3 className="text-xl font-bold mb-2">{snapshot.mainHeadline}</h3>
            {snapshot.subHeadlines.map((headline, index) => (
              <p key={index} className="text-gray-700">{headline}</p>
            ))}
          </div>
          
          <div className="relative">
            <img 
              src={snapshot.fullImageUrl} 
              alt={`${source.name} full homepage`}
              className="w-full rounded-lg border border-gray-200"
            />
          </div>
        </div>
        
        {/* Navigation */}
        <div className="flex justify-between items-center p-4 border-t">
          <button 
            onClick={onPrevious}
            disabled={!hasPrevious}
            className={`flex items-center ${!hasPrevious ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'} px-4 py-2 rounded-lg transition-colors`}
          >
            <ChevronLeft className="w-5 h-5 mr-1" />
            Previous
          </button>
          
          <button 
            onClick={onNext}
            disabled={!hasNext}
            className={`flex items-center ${!hasNext ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-100'} px-4 py-2 rounded-lg transition-colors`}
          >
            Next
            <ChevronRight className="w-5 h-5 ml-1" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default NewsDetail;