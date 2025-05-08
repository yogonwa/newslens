import React, { useState, useEffect } from 'react';
import NewsGrid from '../components/NewsGrid';
import Header from '../components/Header';
import Controls from '../components/Controls';
import Footer from '../components/Footer';
import { STANDARD_TIME_SLOTS } from '../constants/timeSlots';
import { NewsSnapshot, NewsSource } from '../types';
import { useNewsSnapshots } from '../hooks/useNewsSnapshots';
import { useQuery } from '@tanstack/react-query';
import { getNewsSources } from '../services/api';

const Home: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const { data: sources = [], isLoading: isSourcesLoading, isError: isSourcesError } = useQuery<NewsSource[], Error>({
    queryKey: ['newsSources'],
    queryFn: getNewsSources,
  });
  const [activeSourceIds, setActiveSourceIds] = useState<string[]>([]);
  const [selectedDate, setSelectedDate] = useState(new Date());

  // Format selectedDate as YYYY-MM-DD
  const formattedDate = selectedDate.toISOString().slice(0, 10);
  const { data: snapshots = [], isLoading, isError } = useNewsSnapshots(formattedDate);

  useEffect(() => {
    if (sources.length > 0 && activeSourceIds.length === 0) {
      setActiveSourceIds(sources.map(source => source.short_id));
    }
  }, [sources]);

  const toggleSource = (sourceId: string) => {
    setActiveSourceIds(prev =>
      prev.includes(sourceId)
        ? prev.filter(id => id !== sourceId)
        : [...prev, sourceId]
    );
  };
  
  const toggleAllSources = (active: boolean) => {
    if (active) {
      setActiveSourceIds(sources.map(source => source.short_id));
    } else {
      setActiveSourceIds([]);
    }
  };
  
  // Filter sources based on active IDs
  const filteredSources = sources.filter(source => activeSourceIds.includes(source.short_id));
  
  return (
    <div className="flex flex-col min-h-screen">
      <Header onSearchChange={setSearchQuery} />
      
      <main className="flex-grow container mx-auto px-4 pt-28 pb-12">
        <h1 className="text-3xl font-bold mb-2">Media Coverage Comparison</h1>
        <p className="text-gray-600 mb-6">
          See how different news outlets cover the same stories throughout the day.
        </p>
        
        <Controls 
          sources={sources}
          activeSourceIds={activeSourceIds}
          onSourceToggle={toggleSource}
          onToggleAll={toggleAllSources}
          onDateChange={setSelectedDate}
          selectedDate={selectedDate}
        />
        {isSourcesLoading ? (
          <div className="text-center py-12">Loading sources...</div>
        ) : isSourcesError ? (
          <div className="text-center text-red-600 py-12">Failed to load sources</div>
        ) : activeSourceIds.length === 0 ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-8 text-center">
            <p className="text-yellow-800 mb-4">No news sources selected</p>
            <button 
              onClick={() => toggleAllSources(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Show All Sources
            </button>
          </div>
        ) : (
          <NewsGrid 
            snapshots={snapshots}
            sources={filteredSources}
            timeSlots={STANDARD_TIME_SLOTS}
            searchQuery={searchQuery}
          />
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default Home;