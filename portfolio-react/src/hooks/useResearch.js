import { useQuery } from '@tanstack/react-query';
import { getResearch } from '../api/research';
export const useResearch = () => useQuery({ queryKey: ['research'], queryFn: getResearch });
