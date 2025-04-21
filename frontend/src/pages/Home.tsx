import React, { useState } from 'react';
import NewsGrid from '../components/NewsGrid';
import Header from '../components/Header';
import Controls from '../components/Controls';
import Footer from '../components/Footer';
import { newsSources, timeSlots, newsSnapshots } from '../utils/mockData';

const Home: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeSourceIds, setActiveSourceIds] = useState(newsSources.map(source => source.id));
  const [selectedDate, setSelectedDate] = useState(new Date());
  
  const toggleSource = (sourceId: string) => {
    if (activeSourceIds.includes(sourceId)) {
      setActiveSourceIds(activeSourceIds.filter(id => id !== sourceId));
    } else {
      setActiveSourceIds([...activeSourceIds, sourceId]);
    }
  };
  
  const toggleAllSources = (active: boolean) => {
    if (active) {
      setActiveSourceIds(newsSources.map(source => source.id));
    } else {
      setActiveSourceIds([]);
    }
  };
  
  // Filter sources based on active IDs
  const filteredSources = newsSources.filter(source => activeSourceIds.includes(source.id));
  
  return (
    <div className="flex flex-col min-h-screen">
      <Header onSearchChange={setSearchQuery} />
      
      <main className="flex-grow container mx-auto px-4 pt-28 pb-12">
        <h1 className="text-3xl font-bold mb-2">Media Coverage Comparison</h1>
        <p className="text-gray-600 mb-6">
          See how different news outlets cover the same stories throughout the day.
        </p>
        
        <Controls 
          sources={newsSources}
          activeSourceIds={activeSourceIds}
          onSourceToggle={toggleSource}
          onToggleAll={toggleAllSources}
          onDateChange={setSelectedDate}
          selectedDate={selectedDate}
        />
        
        {activeSourceIds.length === 0 ? (
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
            snapshots={newsSnapshots}
            sources={filteredSources}
            timeSlots={timeSlots}
            searchQuery={searchQuery}
          />
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default Home;