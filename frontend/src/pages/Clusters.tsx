import React, { useState, useMemo } from 'react';
import { Filter } from 'lucide-react';
import { newsSnapshots, newsSources } from '../utils/mockData';

interface TopicCluster {
  id: string;
  topic: string;
  keywords: string[];
  sources: {
    sourceId: string;
    headlines: string[];
    sentiment: number;
  }[];
}

const Clusters: React.FC = () => {
  const [selectedCluster, setSelectedCluster] = useState<string | null>(null);

  // Simulate topic clustering with mock data
  const clusters: TopicCluster[] = useMemo(() => [
    {
      id: 'politics',
      topic: 'Political Developments',
      keywords: ['government', 'policy', 'rights', 'president'],
      sources: newsSources.map(source => ({
        sourceId: source.id,
        headlines: newsSnapshots
          .filter(s => s.sourceId === source.id)
          .map(s => s.mainHeadline)
          .filter(h => h.toLowerCase().includes('president') || h.toLowerCase().includes('government')),
        sentiment: newsSnapshots
          .filter(s => s.sourceId === source.id)
          .reduce((acc, s) => acc + s.sentiment.score, 0) / newsSnapshots.length
      }))
    },
    {
      id: 'economy',
      topic: 'Economic News',
      keywords: ['market', 'economy', 'financial', 'business'],
      sources: newsSources.map(source => ({
        sourceId: source.id,
        headlines: newsSnapshots
          .filter(s => s.sourceId === source.id)
          .map(s => s.mainHeadline)
          .filter(h => h.toLowerCase().includes('market') || h.toLowerCase().includes('economic')),
        sentiment: newsSnapshots
          .filter(s => s.sourceId === source.id)
          .reduce((acc, s) => acc + s.sentiment.score, 0) / newsSnapshots.length
      }))
    }
  ], []);

  const getSentimentColor = (score: number) => {
    if (score <= -0.5) return 'bg-red-500';
    if (score < 0) return 'bg-orange-500';
    if (score === 0) return 'bg-gray-500';
    if (score <= 0.5) return 'bg-green-400';
    return 'bg-green-600';
  };

  return (
    <div className="container mx-auto px-4 pt-28 pb-12">
      <h1 className="text-3xl font-bold mb-2">Topic Clusters</h1>
      <p className="text-gray-600 mb-8">
        Discover how different news sources group and frame related stories
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Topic List */}
        <div className="md:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-4">
            <h2 className="text-xl font-semibold mb-4">Topics</h2>
            <div className="space-y-2">
              {clusters.map(cluster => (
                <button
                  key={cluster.id}
                  onClick={() => setSelectedCluster(cluster.id)}
                  className={`w-full text-left px-4 py-3 rounded-md transition-colors ${
                    selectedCluster === cluster.id
                      ? 'bg-blue-50 border border-blue-200'
                      : 'hover:bg-gray-50 border border-gray-200'
                  }`}
                >
                  <h3 className="font-medium">{cluster.topic}</h3>
                  <div className="flex flex-wrap gap-1 mt-2">
                    {cluster.keywords.map(keyword => (
                      <span
                        key={keyword}
                        className="px-2 py-1 bg-gray-100 rounded-full text-xs"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Coverage Analysis */}
        <div className="md:col-span-2">
          {selectedCluster ? (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-6">
                {clusters.find(c => c.id === selectedCluster)?.topic}
              </h2>

              {clusters
                .find(c => c.id === selectedCluster)
                ?.sources.map(source => {
                  const newsSource = newsSources.find(s => s.id === source.sourceId)!;
                  return (
                    <div key={source.sourceId} className="mb-8 last:mb-0">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center">
                          <div
                            className="w-4 h-4 rounded-full mr-2"
                            style={{ backgroundColor: newsSource.color }}
                          ></div>
                          <h3 className="font-medium">{newsSource.name}</h3>
                        </div>
                        <div className={`h-2 w-24 rounded-full ${getSentimentColor(source.sentiment)}`}></div>
                      </div>
                      <div className="space-y-2 pl-6">
                        {source.headlines.map((headline, idx) => (
                          <p key={idx} className="text-gray-600">{headline}</p>
                        ))}
                      </div>
                    </div>
                  );
                })}
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
              Select a topic cluster to see detailed coverage analysis
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Clusters;