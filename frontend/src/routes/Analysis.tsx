import React, { useMemo, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Calendar, Filter, Maximize2, Minimize2 } from 'lucide-react';
import { STANDARD_TIME_SLOTS } from '../constants/timeSlots';
// TODO: Refactor this page for real data integration. All code referencing newsSnapshots, newsSources, or timeSlots is commented out to prevent errors.
// import { newsSnapshots, newsSources, timeSlots } from '../utils/mockData';
// TODO: Refactor this page to use fetchNewsSnapshots or real data.
// All usages of newsSnapshots are commented out for now to prevent runtime errors.
import WordCloud from '../components/WordCloud';

// TODO: Replace with dynamic API data (see /services/api.ts getNewsSources)
const PLACEHOLDER_SOURCES = [
  { id: 'cnn', name: 'CNN', color: '#cc0000' },
  { id: 'foxnews', name: 'Fox News', color: '#003366' },
  { id: 'nytimes', name: 'New York Times', color: '#000000' },
  { id: 'washingtonpost', name: 'Washington Post', color: '#231f20' },
  { id: 'usatoday', name: 'USA Today', color: '#0057b8' },
];

const Analysis: React.FC = () => {
  const [selectedSources, setSelectedSources] = useState<string[]>(PLACEHOLDER_SOURCES.map(s => s.id));
  const [dateRange, setDateRange] = useState({
    start: new Date('2025-05-15'),
    end: new Date('2025-05-15')
  });
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  const sentimentData = useMemo(() => {
    return STANDARD_TIME_SLOTS.map(slot => {
      const slotData = { time: slot.label };
      selectedSources.forEach(sourceId => {
        // const snapshot = newsSnapshots.find(s => s.sourceId === sourceId && s.id.endsWith(`-${slot.id}`));
        if (false) {
          slotData[sourceId] = snapshot.sentiment.score;
        }
      });
      return slotData;
    });
  }, [selectedSources]);

  const { wordCloudData, topWordsBySource } = useMemo(() => {
    const wordsBySource = new Map<string, Map<string, number>>();
    
    // Initialize word counts for each source
    selectedSources.forEach(sourceId => {
      wordsBySource.set(sourceId, new Map<string, number>());
    });
    
    // Count words for each source
    // newsSnapshots.forEach(snapshot => {
    //   if (selectedSources.includes(snapshot.sourceId)) {
    //     const sourceWords = wordsBySource.get(snapshot.sourceId)!;
    //     const allHeadlines = [snapshot.mainHeadline, ...snapshot.subHeadlines].join(' ');
    //     const wordsArray = allHeadlines.toLowerCase()
    //       .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '')
    //       .split(/\s+/)
    //       .filter(word => word.length > 3); // Skip small words
    //     
    //     wordsArray.forEach(word => {
    //       sourceWords.set(word, (sourceWords.get(word) || 0) + 1);
    //     });
    //   }
    // });
    
    // Get top words for each source
    const topWords = new Map<string, { text: string; value: number }[]>();
    wordsBySource.forEach((words, sourceId) => {
      const sortedWords = Array.from(words.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([text, value]) => ({ text, value }));
      topWords.set(sourceId, sortedWords);
    });
    
    // Combine words for word cloud
    const combinedWords = new Map<string, number>();
    selectedSources.forEach(sourceId => {
      const sourceWords = wordsBySource.get(sourceId)!;
      sourceWords.forEach((count, word) => {
        combinedWords.set(word, (combinedWords.get(word) || 0) + count);
      });
    });
    
    const cloudData = Array.from(combinedWords.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 100)
      .map(([text, value]) => ({
        text,
        value: Math.log(value) * 20 // Scale the size logarithmically
      }));
    
    return {
      wordCloudData: cloudData,
      topWordsBySource: topWords
    };
  }, [selectedSources]);

  const toggleSource = (sourceId: string) => {
    setSelectedSources(prev => 
      prev.includes(sourceId)
        ? prev.filter(id => id !== sourceId)
        : [...prev, sourceId]
    );
  };

  const toggleAllSources = () => {
    setSelectedSources(prev => 
      prev.length === PLACEHOLDER_SOURCES.length ? [] : PLACEHOLDER_SOURCES.map(s => s.id)
    );
  };

  const handleDateChange = (date: Date, type: 'start' | 'end') => {
    setDateRange(prev => ({
      ...prev,
      [type]: date
    }));
  };

  return (
    <div className="container mx-auto px-4 pt-28 pb-12">
      <h1 className="text-3xl font-bold mb-8">Sentiment Analysis</h1>
      
      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="flex flex-col sm:flex-row justify-between items-center">
          <div className="flex items-center space-x-4 mb-4 sm:mb-0">
            <div className="flex items-center space-x-2">
              <input
                type="date"
                value={dateRange.start.toISOString().split('T')[0]}
                onChange={(e) => handleDateChange(new Date(e.target.value), 'start')}
                className="px-3 py-2 border rounded-md"
              />
              <span>to</span>
              <input
                type="date"
                value={dateRange.end.toISOString().split('T')[0]}
                onChange={(e) => handleDateChange(new Date(e.target.value), 'end')}
                className="px-3 py-2 border rounded-md"
              />
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <button 
              onClick={() => setIsFilterOpen(!isFilterOpen)}
              className="flex items-center px-3 py-2 bg-gray-100 rounded-md hover:bg-gray-200"
            >
              <Filter size={18} className="mr-2 text-blue-600" />
              <span>Filter Sources</span>
            </button>
            
            <button 
              onClick={toggleAllSources}
              className="flex items-center px-3 py-2 bg-blue-100 rounded-md hover:bg-blue-200"
            >
              {selectedSources.length === PLACEHOLDER_SOURCES.length ? (
                <>
                  <Minimize2 size={18} className="mr-2 text-blue-600" />
                  <span>Hide All</span>
                </>
              ) : (
                <>
                  <Maximize2 size={18} className="mr-2 text-blue-600" />
                  <span>Show All</span>
                </>
              )}
            </button>
          </div>
        </div>
        
        {/* Source filters */}
        {isFilterOpen && (
          <div className="mt-4 pt-4 border-t grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
            {PLACEHOLDER_SOURCES.map((source) => {
              const isActive = selectedSources.includes(source.id);
              return (
                <div 
                  key={source.id} 
                  className={`flex items-center p-2 rounded-md cursor-pointer ${
                    isActive ? 'bg-blue-50 border border-blue-200' : 'bg-gray-50 border border-gray-200'
                  }`}
                  onClick={() => toggleSource(source.id)}
                >
                  <div 
                    className="w-4 h-4 rounded-full mr-2"
                    style={{ backgroundColor: source.color }}
                  ></div>
                  <span className="text-sm">{source.name}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
      
      {/* Sentiment Trends */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Sentiment Trends Over Time</h2>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={sentimentData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis 
                domain={[-1, 1]} 
                ticks={[-1, -0.5, 0, 0.5, 1]}
                label={{ value: 'Sentiment Score', angle: -90, position: 'insideLeft' }} 
              />
              <Tooltip />
              <Legend />
              {selectedSources.map(sourceId => {
                const source = PLACEHOLDER_SOURCES.find(s => s.id === sourceId)!;
                return (
                  <Line
                    key={sourceId}
                    type="monotone"
                    dataKey={sourceId}
                    stroke={source.color}
                    name={source.name}
                    strokeWidth={2}
                  />
                );
              })}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* Word Cloud */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Common Words and Phrases</h2>
        <div className="h-[400px]">
          <WordCloud words={wordCloudData} />
        </div>
      </div>
      
      {/* Top Words Table */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Top Words by Source</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left">Rank</th>
                {selectedSources.map(sourceId => {
                  const source = PLACEHOLDER_SOURCES.find(s => s.id === sourceId)!;
                  return (
                    <th 
                      key={sourceId} 
                      className="px-4 py-2 text-left"
                      style={{ color: source.color }}
                    >
                      {source.name}
                    </th>
                  );
                })}
              </tr>
            </thead>
            <tbody>
              {[0, 1, 2, 3, 4].map(rank => (
                <tr key={rank} className="border-t">
                  <td className="px-4 py-2 font-medium">{rank + 1}</td>
                  {selectedSources.map(sourceId => {
                    const words = topWordsBySource.get(sourceId) || [];
                    const word = words[rank];
                    return (
                      <td key={sourceId} className="px-4 py-2">
                        {word ? (
                          <div className="flex items-center justify-between">
                            <span>{word.text}</span>
                            <span className="text-gray-500 text-sm">({word.value})</span>
                          </div>
                        ) : '-'}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Analysis;