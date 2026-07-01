import { Suspense } from 'react';
import { useProfile } from '../hooks/useProfile';
import HeroSection from '../components/home/HeroSection';
import StatsSection from '../components/home/StatsSection';
import FeaturedProjects from '../components/home/FeaturedProjects';
import SkillsPreview from '../components/home/SkillsPreview';
import CTASection from '../components/home/CTASection';
import SkeletonCard from '../components/ui/SkeletonCard';

export default function HomePage() {
  const { data: profile } = useProfile();
  return (
    <div>
      <HeroSection profile={profile} />
      <StatsSection />
      <FeaturedProjects />
      <SkillsPreview />
      <CTASection profile={profile} />
    </div>
  );
}
