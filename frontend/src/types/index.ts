export interface HeadlineMetadata {
  font_size?: string;
  color?: string;
  is_breaking: boolean;
  editorial_tag?: string;
  subheadline?: string;
  article_url?: string;
}

export interface Headline {
  text: string;
  type: string;
  position: number;
  sentiment?: number;
  metadata?: HeadlineMetadata;
}

export interface Screenshot {
  url: string;
  format: string;
  size: number;
  dimensions: {
    width: number;
    height: number;
  };
  wayback_url?: string;
}

export interface SnapshotMetadata {
  page_title: string;
  url: string;
  wayback_url?: string;
  user_agent: string;
  time_difference: number;
  confidence: string;
  collection_method: string;
  status: string;
  error_message?: string;
  original_timestamp?: string;
}

export interface HeadlineSnapshot {
  _id: string;
  source_id: string;
  display_timestamp: string;
  actual_timestamp: string;
  headlines: Headline[];
  screenshot: Screenshot;
  metadata: SnapshotMetadata;
  created_at: string;
  updated_at: string;
}

export interface SourceMetadata {
  screenshot_path?: string;
  last_updated?: string;
  timezone: string;
  user_agent: string;
  created_at: string;
  updated_at: string;
  wayback_enabled: boolean;
  live_scrape_enabled: boolean;
}

export interface NewsSource {
  _id: string;
  name: string;
  url: string;
  active: boolean;
  metadata: SourceMetadata;
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