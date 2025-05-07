import { useQuery } from '@tanstack/react-query';
import { getNewsSnapshots } from '../services/api';
import { NewsSnapshot } from '../types';

export const useNewsSnapshots = (date: string) => {
  return useQuery<NewsSnapshot[], Error>({
    queryKey: ['newsSnapshots', date],
    queryFn: () => getNewsSnapshots(date),
    enabled: !!date,
  });
}; 