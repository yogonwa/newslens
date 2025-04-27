import { NewsSource, NewsSnapshot, TimeSlot } from '../types';

export const newsSources = [
  {
    _id: 'cnn',
    name: 'CNN',
    url: 'https://cnn.com',
    active: true,
    metadata: {
      timezone: 'America/New_York',
      user_agent: '',
      created_at: '',
      updated_at: '',
      wayback_enabled: true,
      live_scrape_enabled: false,
    },
    color: '#CC0000',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/CNN_International_logo.svg/1200px-CNN_International_logo.svg.png',
  },
  {
    _id: 'fox',
    name: 'Fox News',
    url: 'https://foxnews.com',
    active: true,
    metadata: {
      timezone: 'America/New_York',
      user_agent: '',
      created_at: '',
      updated_at: '',
      wayback_enabled: true,
      live_scrape_enabled: false,
    },
    color: '#003366',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Fox_News_Channel_logo.svg/1200px-Fox_News_Channel_logo.svg.png',
  },
  {
    _id: 'nytimes',
    name: 'New York Times',
    url: 'https://nytimes.com',
    active: true,
    metadata: {
      timezone: 'America/New_York',
      user_agent: '',
      created_at: '',
      updated_at: '',
      wayback_enabled: true,
      live_scrape_enabled: false,
    },
    color: '#000000',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/NewYorkTimes.svg/1200px-NewYorkTimes.svg.png',
  },
  {
    _id: 'usatoday',
    name: 'USA Today',
    url: 'https://usatoday.com',
    active: true,
    metadata: {
      timezone: 'America/New_York',
      user_agent: '',
      created_at: '',
      updated_at: '',
      wayback_enabled: true,
      live_scrape_enabled: false,
    },
    color: '#00529B',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/USA_Today_Logo.svg/1200px-USA_Today_Logo.svg.png',
  },
  {
    _id: 'wapo',
    name: 'Washington Post',
    url: 'https://washingtonpost.com',
    active: true,
    metadata: {
      timezone: 'America/New_York',
      user_agent: '',
      created_at: '',
      updated_at: '',
      wayback_enabled: true,
      live_scrape_enabled: false,
    },
    color: '#231F20',
    logoUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Washington_Post_logo_2015.svg/1200px-Washington_Post_logo_2015.svg.png',
  },
];

export const timeSlots: TimeSlot[] = [
  { id: '20250418-0600', label: '6 AM', time: '06:00' },
  { id: '20250418-0900', label: '9 AM', time: '09:00' },
  { id: '20250418-1200', label: '12 PM', time: '12:00' },
  { id: '20250418-1500', label: '3 PM', time: '15:00' },
  { id: '20250418-1800', label: '6 PM', time: '18:00' }
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
      const randomSeed = (source._id.charCodeAt(0) + parseInt(timeSlot.id)) % 1000;
      
      snapshots.push({
        id: `${source._id}-${timeSlot.id}`,
        sourceId: source._id,
        timestamp: `2025-05-15T${timeSlot.time}:00`,
        thumbnailUrl: `https://picsum.photos/seed/${source._id}${timeSlot.id}/300/200`,
        fullImageUrl: `https://picsum.photos/seed/${source._id}${timeSlot.id}/1200/800`,
        mainHeadline: generateMockHeadlines(source._id, timeSlot.id)[0],
        subHeadlines: [generateMockHeadlines(source._id, timeSlot.id)[1]],
        sentiment: generateSentiment(source._id, timeSlot.id),
      });
    });
  });

  return snapshots;
};

export const fetchNewsSnapshots = async (): Promise<NewsSnapshot[]> => {
  const res = await fetch('http://localhost:8000/snapshots');
  const data = await res.json();
  // Map API response to NewsSnapshot type
  return data.map((item: any) => ({
    id: item.id,
    sourceId: item.sourceId,
    timestamp: item.timestamp,
    thumbnailUrl: item.thumbnailUrl,
    fullImageUrl: item.imageUrl,
    mainHeadline: item.mainHeadline,
    subHeadlines: item.subHeadlines,
    sentiment: { score: 0, magnitude: 0.5 }, // Placeholder for now
  }));
};

export const getCurrentDate = (): string => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};