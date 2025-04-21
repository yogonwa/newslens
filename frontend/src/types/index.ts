export interface NewsSource {
  id: string;
  name: string;
  logoUrl: string;
  color: string;
}

export interface NewsSnapshot {
  id: string;
  sourceId: string;
  timestamp: string;
  thumbnailUrl: string;
  fullImageUrl: string;
  mainHeadline: string;
  subHeadlines: string[];
  sentiment: {
    score: number; // -1 to 1, negative to positive
    magnitude: number; // 0 to 1, intensity
  };
}

export interface TimeSlot {
  id: string;
  label: string;
  time: string;
}