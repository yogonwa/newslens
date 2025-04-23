import axios from 'axios';
import { NewsSource, HeadlineSnapshot } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getNewsSources = async (): Promise<NewsSource[]> => {
  const response = await api.get('/sources');
  return response.data;
};

export const getHeadlineSnapshots = async (params: {
  sourceIds?: string[];
  date?: string;
  startTime?: string;
  endTime?: string;
}): Promise<HeadlineSnapshot[]> => {
  const response = await api.get('/headlines', { params });
  return response.data;
};

export const getLatestHeadlines = async (sourceIds?: string[]): Promise<HeadlineSnapshot[]> => {
  const response = await api.get('/headlines/latest', {
    params: { sourceIds: sourceIds?.join(',') }
  });
  return response.data;
}; 