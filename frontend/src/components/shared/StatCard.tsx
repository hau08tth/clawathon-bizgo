import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  gradient: string;
  trend?: { value: number; label: string };
}

export default function StatCard({ title, value, subtitle, icon: Icon, gradient, trend }: StatCardProps) {
  return (
    <div className={cn("relative overflow-hidden rounded-2xl p-6 text-white shadow-lg card-hover", gradient)}>
      <div className="absolute top-0 right-0 w-32 h-32 rounded-full bg-white/10 -mr-8 -mt-8" />
      <div className="absolute bottom-0 left-0 w-20 h-20 rounded-full bg-white/10 -ml-6 -mb-6" />
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm font-medium text-white/80">{title}</p>
          <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center">
            <Icon className="w-5 h-5 text-white" />
          </div>
        </div>
        <p className="text-3xl font-bold">{value}</p>
        {subtitle && <p className="text-sm text-white/70 mt-1">{subtitle}</p>}
        {trend && (
          <div className="mt-3 flex items-center gap-1 text-xs">
            <span className="text-white/80">
              {trend.value >= 0 ? "↑" : "↓"} {Math.abs(trend.value)}%
            </span>
            <span className="text-white/60">{trend.label}</span>
          </div>
        )}
      </div>
    </div>
  );
}
