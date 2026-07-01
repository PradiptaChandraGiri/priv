import { useQuery } from '@tanstack/react-query';
import { getSkills } from '../api/skills';
export const useSkills = () => useQuery({ queryKey: ['skills'], queryFn: getSkills });
