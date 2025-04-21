import { NewsSource, NewsSnapshot, TimeSlot } from '../types';

export const newsSources: NewsSource[] = [
  {
    id: 'cnn',
    name: 'CNN',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/CNN_International_logo.svg/1200px-CNN_International_logo.svg.png',
    color: '#CC0000',
  },
  {
    id: 'fox',
    name: 'Fox News',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Fox_News_Channel_logo.svg/1200px-Fox_News_Channel_logo.svg.png',
    color: '#003366',
  },
  {
    id: 'nyt',
    name: 'New York Times',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/NewYorkTimes.svg/1200px-NewYorkTimes.svg.png',
    color: '#000000',
  },
  {
    id: 'wsj',
    name: 'Wall Street Journal',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/WSJ.svg/1200px-WSJ.svg.png',
    color: '#0274B6',
  },
  {
    id: 'bbc',
    name: 'BBC News',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/BBC_News_2019.svg/1200px-BBC_News_2019.svg.png',
    color: '#BB1919',
  },
];

export const timeSlots: TimeSlot[] = [
  { id: '1', label: '6 AM', time: '06:00' },
  { id: '2', label: '9 AM', time: '09:00' },
  { id: '3', label: '12 PM', time: '12:00' },
  { id: '4', label: '3 PM', time: '15:00' },
  { id: '5', label: '6 PM', time: '18:00' },
  { id: '6', label: '9 PM', time: '21:00' },
];

// For demo purposes, we're using Pexels for news homepage screenshots
// In a real implementation, these would be actual screenshots from news sources
const generateMockHeadlines = (sourceId: string, timeSlot: string): string[] => {
  const headlinesBySource: Record<string, Record<string, string[]>> = {
    cnn: {
      '1': ['Global Tensions Rise as Talks Collapse', 'Market Plunges Amid Economic Uncertainty'],
      '2': ['Breaking: Government Announces New Stimulus Package', 'Healthcare Reform Bill Faces Opposition'],
      '3': ['President Addresses Nation on Climate Crisis', 'Tech Giants Face Antitrust Investigation'],
      '4': ['Protests Erupt in Major Cities Nationwide', 'Hurricane Warning Issued for Coastal Regions'],
      '5': ['Global Summit Reaches Historic Agreement', 'Supreme Court Rules on Controversial Case'],
      '6': ['Election Results: What They Mean for the Country', 'Sports: Championship Finals Tonight'],
    },
    fox: {
      '1': ['Border Crisis Intensifies as Policy Fails', 'Government Spending Reaches Record High'],
      '2': ['Tax Cuts Proposed to Boost Economy', 'Constitutional Rights Under Threat, Experts Say'],
      '3': ['President\'s Climate Agenda Criticized by Industry Leaders', 'Small Businesses Struggle Under Regulations'],
      '4': ['Law Enforcement Responds to Urban Unrest', 'Weather Alert: Storm System Approaching South'],
      '5': ['Analysis: Summit Agreement Surrenders Sovereignty', 'Justice: Court Decision Upends Precedent'],
      '6': ['Election Night Coverage: Change Coming to Washington', 'Championship Game: Underdog Story'],
    },
    nyt: {
      '1': ['Diplomatic Efforts Falter as Global Tensions Mount', 'Economic Indicators Signal Potential Downturn'],
      '2': ['Administration Unveils Economic Relief Measures', 'Analysis: The Politics of Healthcare Reform'],
      '3': ['In Address, President Outlines Climate Initiative', 'Regulatory Scrutiny Intensifies for Technology Sector'],
      '4': ['Civil Unrest: The Roots of National Protests', 'Scientists Track Strengthening Hurricane System'],
      '5': ['Behind the Scenes: How the Summit Agreement Was Reached', 'Court\'s Ruling Reshapes Legal Landscape'],
      '6': ['The Vote: A Detailed Analysis of Election Outcomes', 'Cultural Moment: Sports Finals Capture Nation\'s Attention'],
    },
    wsj: {
      '1': ['Markets React as International Relations Deteriorate', 'Investors Brace for Economic Volatility'],
      '2': ['Fiscal Policy: New Stimulus and Market Implications', 'Healthcare Sector Responds to Reform Proposals'],
      '3': ['Business Impact: Analyzing the Climate Policy Shift', 'Tech Stocks Fluctuate Amid Regulatory Concerns'],
      '4': ['Economic Impact of National Protests Assessed', 'Insurance Sector Prepares for Storm Response'],
      '5': ['Global Agreement: Trade and Financial Implications', 'Legal Analysis: The Court\'s Decision and Business'],
      '6': ['Elections and Markets: The Economic Outlook', 'Sports Business: The Financial Stakes of Championship'],
    },
    bbc: {
      '1': ['Global Diplomacy in Crisis as Talks Break Down', 'Financial Markets: Worldwide Uncertainty Grows'],
      '2': ['American Government Announces Economic Measures', 'Health Policy Debate Intensifies in the States'],
      '3': ['Climate Crisis: Presidential Address Sets New Direction', 'Technology Giants Face Increased Scrutiny'],
      '4': ['Analysis: Protest Movements Across America', 'Weather Alert: Tracking the Developing Hurricane'],
      '5': ['Historic Accord Reached at International Summit', 'Supreme Court Verdict: International Reactions'],
      '6': ['US Election Results: Global Implications', 'Sports Final Draws International Audience'],
    },
  };

  return headlinesBySource[sourceId]?.[timeSlot] || ['Default Headline'];
};

const generateSentiment = (sourceId: string, timeSlot: string): { score: number; magnitude: number } => {
  // This would be replaced with actual sentiment analysis in a real implementation
  const sentimentBySource: Record<string, Record<string, { score: number; magnitude: number }>> = {
    cnn: {
      '1': { score: -0.4, magnitude: 0.8 },
      '2': { score: 0.2, magnitude: 0.5 },
      '3': { score: -0.1, magnitude: 0.3 },
      '4': { score: -0.6, magnitude: 0.9 },
      '5': { score: 0.7, magnitude: 0.8 },
      '6': { score: 0.1, magnitude: 0.4 },
    },
    fox: {
      '1': { score: -0.6, magnitude: 0.9 },
      '2': { score: -0.3, magnitude: 0.7 },
      '3': { score: -0.5, magnitude: 0.8 },
      '4': { score: -0.4, magnitude: 0.6 },
      '5': { score: -0.2, magnitude: 0.5 },
      '6': { score: 0.3, magnitude: 0.4 },
    },
    nyt: {
      '1': { score: -0.3, magnitude: 0.5 },
      '2': { score: 0.1, magnitude: 0.4 },
      '3': { score: 0.2, magnitude: 0.6 },
      '4': { score: -0.2, magnitude: 0.7 },
      '5': { score: 0.4, magnitude: 0.5 },
      '6': { score: 0.0, magnitude: 0.3 },
    },
    wsj: {
      '1': { score: -0.2, magnitude: 0.4 },
      '2': { score: 0.3, magnitude: 0.3 },
      '3': { score: -0.1, magnitude: 0.2 },
      '4': { score: -0.3, magnitude: 0.5 },
      '5': { score: 0.2, magnitude: 0.4 },
      '6': { score: 0.1, magnitude: 0.3 },
    },
    bbc: {
      '1': { score: -0.3, magnitude: 0.6 },
      '2': { score: 0.0, magnitude: 0.4 },
      '3': { score: -0.1, magnitude: 0.5 },
      '4': { score: -0.5, magnitude: 0.7 },
      '5': { score: 0.5, magnitude: 0.6 },
      '6': { score: 0.0, magnitude: 0.4 },
    },
  };

  return sentimentBySource[sourceId]?.[timeSlot] || { score: 0, magnitude: 0.5 };
};

export const generateMockData = (): NewsSnapshot[] => {
  const snapshots: NewsSnapshot[] = [];

  newsSources.forEach((source) => {
    timeSlots.forEach((timeSlot) => {
      // Generate a unique yet consistent random number for each source/timeSlot combination
      const randomSeed = (source.id.charCodeAt(0) + parseInt(timeSlot.id)) % 1000;
      
      snapshots.push({
        id: `${source.id}-${timeSlot.id}`,
        sourceId: source.id,
        timestamp: `2025-05-15T${timeSlot.time}:00`,
        thumbnailUrl: `https://picsum.photos/seed/${source.id}${timeSlot.id}/300/200`,
        fullImageUrl: `https://picsum.photos/seed/${source.id}${timeSlot.id}/1200/800`,
        mainHeadline: generateMockHeadlines(source.id, timeSlot.id)[0],
        subHeadlines: [generateMockHeadlines(source.id, timeSlot.id)[1]],
        sentiment: generateSentiment(source.id, timeSlot.id),
      });
    });
  });

  return snapshots;
};

export const newsSnapshots = generateMockData();

export const getSnapshotsByTimeSlot = (timeSlotId: string): NewsSnapshot[] => {
  return newsSnapshots.filter((snapshot) => snapshot.id.endsWith(`-${timeSlotId}`));
};

export const getSnapshotsBySource = (sourceId: string): NewsSnapshot[] => {
  return newsSnapshots.filter((snapshot) => snapshot.sourceId === sourceId);
};

export const getSnapshot = (id: string): NewsSnapshot | undefined => {
  return newsSnapshots.find((snapshot) => snapshot.id === id);
};

export const getCurrentDate = (): string => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};