import { useQuery } from '@tanstack/react-query';
import { getCertificates } from '../api/certificates';
export const useCertificates = (params) => useQuery({ queryKey: ['certificates', params], queryFn: () => getCertificates(params) });
