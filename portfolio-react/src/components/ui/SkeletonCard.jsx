export default function SkeletonCard({ height='h-64' }) {
  return (
    <div className={`rounded-lg border border-white/10 overflow-hidden ${height}`}>
      <div className="skeleton-shimmer h-1/2 rounded-none" />
      <div className="p-4 space-y-3">
        <div className="skeleton-shimmer h-3 w-2/3 rounded" />
        <div className="skeleton-shimmer h-3 w-full rounded" />
        <div className="skeleton-shimmer h-3 w-4/5 rounded" />
        <div className="flex gap-2 mt-4">
          {[1,2,3].map(i => <div key={i} className="skeleton-shimmer h-5 w-12 rounded-full" />)}
        </div>
      </div>
    </div>
  );
}
