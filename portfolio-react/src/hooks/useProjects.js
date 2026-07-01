import { useQuery } from '@tanstack/react-query';
import { getProjects } from '../api/projects';
export const useProjects = (params) => useQuery({ queryKey: ['projects', params], queryFn: () => getProjects(params) });
