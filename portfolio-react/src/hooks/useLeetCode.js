import { useQuery } from '@tanstack/react-query';
import { fetchLeetCodeProfile, fetchLeetCodeRecentSubmissions } from '../api/leetcode';

export const useLeetCodeProfile = (username) => {
  return useQuery({
    queryKey: ['leetcode-profile', username],
    queryFn: () => fetchLeetCodeProfile(username),
    enabled: !!username,
    staleTime: 10 * 60 * 1000,
    retry: 2,
  });
};

export const useLeetCodeSubmissions = (username) => {
  return useQuery({
    queryKey: ['leetcode-submissions', username],
    queryFn: () => fetchLeetCodeRecentSubmissions(username, 15),
    enabled: !!username,
    staleTime: 10 * 60 * 1000,
    retry: 2,
  });
};
