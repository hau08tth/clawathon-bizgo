"use client";
import { useEffect, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { gamificationApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import { Trophy, Crown, Medal, Star } from "lucide-react";
import { formatCoins, DEPARTMENT_LABELS } from "@/lib/utils";
import { cn } from "@/lib/utils";

interface LeaderEntry {
  rank: number;
  id: string;
  full_name: string;
  department: string;
  position: string;
  avatar_url?: string;
  bizcoins: number;
  badges: { name: string; icon: string; color: string }[];
}

const RANK_STYLES = [
  { bg: "from-amber-400 to-yellow-300", text: "🥇", shadow: "shadow-amber-200", label: "Champion" },
  { bg: "from-gray-400 to-gray-300", text: "🥈", shadow: "shadow-gray-200", label: "Runner-up" },
  { bg: "from-orange-400 to-amber-300", text: "🥉", shadow: "shadow-orange-200", label: "3rd Place" },
];

export default function LeaderboardPage() {
  const { employee } = useAppStore();
  const [leaderboard, setLeaderboard] = useState<LeaderEntry[]>([]);
  const [myStats, setMyStats] = useState<{ rank: number; bizcoins: number }>({ rank: 0, bizcoins: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([gamificationApi.leaderboard(), gamificationApi.myStats()]).then(([lb, s]) => {
      setLeaderboard(lb.data);
      setMyStats(s.data);
      setLoading(false);
    });
  }, []);

  if (loading) return (
    <AppShell>
      <div className="flex items-center justify-center h-screen">
        <div className="w-12 h-12 border-4 border-amber-300 border-t-amber-600 rounded-full animate-spin" />
      </div>
    </AppShell>
  );

  const top3 = leaderboard.slice(0, 3);
  const rest = leaderboard.slice(3);

  return (
    <AppShell>
      <div className="p-8 max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="w-16 h-16 rounded-2xl gradient-gold flex items-center justify-center mx-auto mb-4 shadow-xl">
            <Trophy className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-black text-gray-900">BizGro Leaderboard</h1>
          <p className="text-gray-500 mt-1">Bảng xếp hạng BizCoins thời gian thực</p>
        </div>

        {/* My rank banner */}
        <div className="mb-8 bg-gradient-to-r from-violet-500 to-purple-600 rounded-2xl p-5 text-white text-center shadow-lg">
          <p className="text-sm font-medium text-white/80">Vị trí của bạn</p>
          <p className="text-4xl font-black">#{myStats.rank}</p>
          <p className="text-white/80">{formatCoins(myStats.bizcoins)} BizCoins</p>
        </div>

        {/* Top 3 podium */}
        {top3.length >= 3 && (
          <div className="grid grid-cols-3 gap-4 mb-6 items-end">
            {/* 2nd place */}
            <div className="text-center">
              <div className="mx-auto w-16 h-16 rounded-full bg-gradient-to-b from-gray-300 to-gray-400 flex items-center justify-center text-2xl shadow-lg mb-2">
                {top3[1]?.full_name.charAt(0)}
              </div>
              <p className="font-bold text-sm text-gray-800 truncate">{top3[1]?.full_name}</p>
              <p className="text-xs text-gray-500">{DEPARTMENT_LABELS[top3[1]?.department] || top3[1]?.department}</p>
              <div className="mt-2 bg-gray-100 rounded-2xl py-6 px-3">
                <p className="text-2xl">🥈</p>
                <p className="font-black text-gray-700">{formatCoins(top3[1]?.bizcoins)}</p>
                <p className="text-xs text-gray-400">BizCoins</p>
              </div>
            </div>
            {/* 1st place */}
            <div className="text-center -mt-4">
              <div className="flex justify-center mb-1">
                <Crown className="w-6 h-6 text-amber-400" />
              </div>
              <div className="mx-auto w-20 h-20 rounded-full bg-gradient-to-b from-amber-300 to-yellow-400 flex items-center justify-center text-3xl shadow-xl mb-2 ring-4 ring-amber-200">
                {top3[0]?.full_name.charAt(0)}
              </div>
              <p className="font-bold text-sm text-gray-800 truncate">{top3[0]?.full_name}</p>
              <p className="text-xs text-gray-500">{DEPARTMENT_LABELS[top3[0]?.department] || top3[0]?.department}</p>
              <div className="mt-2 gradient-gold rounded-2xl py-8 px-3 shadow-lg shadow-amber-200">
                <p className="text-3xl">🥇</p>
                <p className="font-black text-white text-xl">{formatCoins(top3[0]?.bizcoins)}</p>
                <p className="text-xs text-white/80">BizCoins</p>
              </div>
            </div>
            {/* 3rd place */}
            <div className="text-center">
              <div className="mx-auto w-16 h-16 rounded-full bg-gradient-to-b from-orange-300 to-amber-400 flex items-center justify-center text-2xl shadow-lg mb-2">
                {top3[2]?.full_name.charAt(0)}
              </div>
              <p className="font-bold text-sm text-gray-800 truncate">{top3[2]?.full_name}</p>
              <p className="text-xs text-gray-500">{DEPARTMENT_LABELS[top3[2]?.department] || top3[2]?.department}</p>
              <div className="mt-2 bg-orange-50 rounded-2xl py-6 px-3">
                <p className="text-2xl">🥉</p>
                <p className="font-black text-orange-600">{formatCoins(top3[2]?.bizcoins)}</p>
                <p className="text-xs text-gray-400">BizCoins</p>
              </div>
            </div>
          </div>
        )}

        {/* Rest of leaderboard */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-4 border-b border-gray-100 bg-gray-50">
            <div className="grid grid-cols-12 text-xs font-semibold text-gray-400 uppercase tracking-wider">
              <span className="col-span-1">Hạng</span>
              <span className="col-span-5">Nhân viên</span>
              <span className="col-span-3">Phòng ban</span>
              <span className="col-span-3 text-right">BizCoins</span>
            </div>
          </div>
          {rest.map((entry) => (
            <div
              key={entry.id}
              className={cn(
                "p-4 border-b border-gray-50 last:border-0 grid grid-cols-12 items-center",
                entry.id === employee?.id ? "bg-violet-50" : "hover:bg-gray-50"
              )}
            >
              <div className="col-span-1">
                <span className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm font-bold text-gray-600">
                  {entry.rank}
                </span>
              </div>
              <div className="col-span-5 flex items-center gap-3">
                <div className="w-9 h-9 rounded-full gradient-bizgro flex items-center justify-center text-white text-sm font-bold shadow">
                  {entry.full_name.charAt(0)}
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-800">
                    {entry.full_name}
                    {entry.id === employee?.id && (
                      <span className="ml-2 text-xs text-violet-600 font-normal">(bạn)</span>
                    )}
                  </p>
                  {entry.badges.length > 0 && (
                    <div className="flex gap-1 mt-0.5">
                      {entry.badges.slice(0, 2).map((b, i) => (
                        <span key={i} className="text-xs" title={b.name}>{b.icon}</span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
              <div className="col-span-3">
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                  {DEPARTMENT_LABELS[entry.department] || entry.department}
                </span>
              </div>
              <div className="col-span-3 text-right">
                <span className="font-bold text-amber-600">
                  🪙 {formatCoins(entry.bizcoins)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
