import React, { useState } from 'react';
import { NewsSnapshot, NewsSource, TimeSlot } from '../types';
import NewsCell from './NewsCell';
import NewsDetail from './NewsDetail';

interface NewsGridProps {
  snapshots: NewsSnapshot[];
  sources: NewsSource[];
  timeSlots: TimeSlot[];
  searchQuery: string;
}

const NewsGrid: React.FC<NewsGridProps> = ({ snapshots, sources, timeSlots, searchQuery }) => {
  const [selectedSnapshot, setSelectedSnapshot] = useState<NewsSnapshot | null>(null);
  
  const getSourceById = (id: string): NewsSource => {
    return sources.find(source => source._id === id) || sources[0];
  };

  const getSnapshotsByTimeSlot = (timeSlotId: string): NewsSnapshot[] => {
    return snapshots.filter(snapshot => snapshot.id.endsWith(`-${timeSlotId}`));
  };

  // Filter snapshots based on search query
  const filteredSnapshots = searchQuery.trim() === '' 
    ? snapshots 
    : snapshots.filter(snapshot => {
        const lowerQuery = searchQuery.toLowerCase();
        return (
          snapshot.mainHeadline.toLowerCase().includes(lowerQuery) || 
          snapshot.subHeadlines.some(headline => headline.toLowerCase().includes(lowerQuery))
        );
      });

  // Get the current snapshot's index for navigation
  const currentIndex = selectedSnapshot 
    ? filteredSnapshots.findIndex(snapshot => snapshot.id === selectedSnapshot.id)
    : -1;

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setSelectedSnapshot(filteredSnapshots[currentIndex - 1]);
    }
  };

  const handleNext = () => {
    if (currentIndex < filteredSnapshots.length - 1) {
      setSelectedSnapshot(filteredSnapshots[currentIndex + 1]);
    }
  };

  return (
    <div className="w-full">
      {/* Time slot headers */}
      <div className="flex">
        <div className="w-36 flex-shrink-0"></div>
        <div className="flex-1 grid grid-cols-5 gap-4">
          {timeSlots.map((slot) => (
            <div key={slot.id} className="text-center">
              <h3 className="font-medium text-gray-800">{slot.label}</h3>
            </div>
          ))}
        </div>
      </div>
      
      {/* Source rows */}
      {sources.map((source) => (
        <div key={source._id} className="flex mb-8">
          {/* Source name column */}
          <div className="w-36 flex-shrink-0 pr-4 flex items-center">
            <div className="flex items-center">
              <div className="w-3 h-12 rounded-full mr-2" style={{ backgroundColor: source.color }}></div>
              <span className="font-medium">{source.name}</span>
            </div>
          </div>
          
          {/* News snapshots grid */}
          <div className="flex-1 grid grid-cols-5 gap-4">
            {timeSlots.map((slot) => {
              const snapshotsForTimeSlot = getSnapshotsByTimeSlot(slot.id);
              const snapshotForSource = snapshotsForTimeSlot.find(
                snapshot => snapshot.sourceId === source._id
              );
              
              // Skip rendering if filtered out by search
              if (
                searchQuery.trim() !== '' && 
                snapshotForSource && 
                !filteredSnapshots.some(s => s.id === snapshotForSource.id)
              ) {
                return (
                  <div key={`${source._id}-${slot.id}`} className="h-48 rounded-lg border-2 border-dashed border-gray-200 flex items-center justify-center text-gray-400 text-sm">
                    No match
                  </div>
                );
              }
              
              return snapshotForSource ? (
                <div key={`${source._id}-${slot.id}`} className="transition-all duration-300">
                  <NewsCell 
                    snapshot={snapshotForSource} 
                    source={source}
                    onClick={() => setSelectedSnapshot(snapshotForSource)}
                  />
                </div>
              ) : (
                <div key={`${source._id}-${slot.id}`} className="h-48 rounded-lg border-2 border-dashed border-gray-200 flex items-center justify-center text-gray-400">
                  No data
                </div>
              );
            })}
          </div>
        </div>
      ))}
      
      {/* Detail view */}
      {selectedSnapshot && (
        <NewsDetail 
          snapshot={selectedSnapshot}
          source={getSourceById(selectedSnapshot.sourceId)}
          onClose={() => setSelectedSnapshot(null)}
          onPrevious={handlePrevious}
          onNext={handleNext}
          hasPrevious={currentIndex > 0}
          hasNext={currentIndex < filteredSnapshots.length - 1}
        />
      )}
    </div>
  );
};

export default NewsGrid;