"use client";
import { useEffect, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import StatCard from "@/components/shared/StatCard";
import { gamificationApi, bizShareApi, bizCoCreateApi, bizConnectApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import { formatCoins, formatDate, DEPARTMENT_LABELS } from "@/lib/utils";
import { Coins, Share2, Network, Lightbulb, Trophy, TrendingUp, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
  const { employee } = useAppStore();
  const [stats, setStats] = useState<{
    bizcoins: number; rank: number; total_earned: number;
    badges: unknown[];
    recent_transactions?: Array<{ type: string; amount: number; reason: string; created_at: string }>;
  }>({ bizcoins: 0, rank: 0, total_earned: 0, badges: [] });
  const [posts, setPosts] = useState<unknown[]>([]);
  const [ideas, setIdeas] = useState<unknown[]>([]);
  const [opportunities, setOpportunities] = useState<unknown[]>([]);
  const [leaderboard, setLeaderboard] = useState<unknown[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [s, p, i, o, lb] = await Promise.all([
          gamificationApi.myStats(),
          bizShareApi.myPosts(),
          bizCoCreateApi.myIdeas(),
          bizConnectApi.opportunities(),
          gamificationApi.leaderboard(),
        ]);
        setStats(s.data);
        setPosts(p.data);
        setIdeas(i.data);
        setOpportunities(o.data);
        setLeaderboard(lb.data.slice(0, 5));
      } catch { /* ignore */ }
      setLoading(false);
    };
    load();
  }, []);

  if (loading) return (
    <AppShell>
      <div className="flex items-center justify-center h-screen">
        <div className="w-12 h-12 border-4 border-violet-300 border-t-violet-600 rounded-full animate-spin" />
      </div>
    </AppShell>
  );

  return (
    <AppShell>
      <div className="p-8 max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Xin chào, {employee?.full_name?.split(" ").slice(-1)[0]} 👋
          </h1>
          <p className="text-gray-500 mt-1">
            {DEPARTMENT_LABELS[employee?.department || "tech"]} •{" "}
            {employee?.position || "Employee"}
          </p>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            title="BizCoins"
            value={formatCoins(stats.bizcoins)}
            subtitle={`Hạng #${stats.rank}`}
            icon={Coins}
            gradient="gradient-gold"
            trend={{ value: 12, label: "tháng này" }}
          />
          <StatCard
            title="Bài đăng"
            value={(posts as unknown[]).length}
            subtitle="Chiến dịch đã tham gia"
            icon={Share2}
            gradient="gradient-bizshare"
          />
          <StatCard
            title="Kết nối B2B"
            value={(opportunities as unknown[]).length}
            subtitle="Cơ hội được tạo"
            icon={Network}
            gradient="gradient-bizconnect"
          />
          <StatCard
            title="Ý tưởng"
            value={(ideas as unknown[]).length}
            subtitle="Đã gửi lên"
            icon={Lightbulb}
            gradient="gradient-bizcocreate"
          />
        </div>

        {/* Main content grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Quick Actions */}
          <div className="lg:col-span-2 space-y-4">
            <h2 className="text-lg font-bold text-gray-800">Bắt đầu ngay</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {[
                {
                  href: "/biz-share",
                  icon: "📢",
                  title: "BIZ-SHARE",
                  desc: "Tạo content AI & chia sẻ chiến dịch",
                  gradient: "gradient-bizshare",
                  coins: "+10 BizCoins",
                },
                {
                  href: "/biz-connect",
                  icon: "🤝",
                  title: "BIZ-CONNECT",
                  desc: "Kết nối mạng lưới quan hệ B2B",
                  gradient: "gradient-bizconnect",
                  coins: "+200 BizCoins",
                },
                {
                  href: "/biz-cocreate",
                  icon: "💡",
                  title: "BIZ-COCREATE",
                  desc: "Gửi ý tưởng, nhận đề xuất AI",
                  gradient: "gradient-bizcocreate",
                  coins: "+500 BizCoins",
                },
              ].map((m) => (
                <Link
                  key={m.href}
                  href={m.href}
                  className="group bg-white rounded-2xl p-5 shadow-sm hover:shadow-md transition-all border border-gray-100 card-hover"
                >
                  <div className={`w-12 h-12 rounded-xl ${m.gradient} flex items-center justify-center text-2xl mb-3 shadow-md`}>
                    {m.icon}
                  </div>
                  <h3 className="font-bold text-gray-800 text-sm">{m.title}</h3>
                  <p className="text-xs text-gray-500 mt-1 mb-3">{m.desc}</p>
                  <span className="text-xs font-semibold text-amber-600 bg-amber-50 px-2 py-1 rounded-full">
                    {m.coins}
                  </span>
                </Link>
              ))}
            </div>

            {/* Recent transactions */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-gray-800">Lịch sử điểm thưởng</h3>
                <TrendingUp className="w-4 h-4 text-gray-400" />
              </div>
              {stats.recent_transactions?.length === 0 ? (
                <p className="text-sm text-gray-400 text-center py-4">
                  Chưa có giao dịch nào. Bắt đầu kiếm BizCoins ngay!
                </p>
              ) : (
                <div className="space-y-3">
                  {(stats.recent_transactions as Array<{ type: string; amount: number; reason: string; created_at: string }>)?.slice(0, 5).map((tx, i) => (
                    <div key={i} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                      <div>
                        <p className="text-sm font-medium text-gray-800">{tx.reason}</p>
                        <p className="text-xs text-gray-400">{formatDate(tx.created_at)}</p>
                      </div>
                      <span className={`text-sm font-bold ${tx.type === "earn" ? "text-green-600" : "text-red-500"}`}>
                        {tx.type === "earn" ? "+" : "-"}{tx.amount} 🪙
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Leaderboard mini */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-gray-800 flex items-center gap-2">
                <Trophy className="w-4 h-4 text-amber-500" /> Top Stars
              </h3>
              <Link href="/leaderboard" className="text-xs text-violet-600 hover:underline flex items-center gap-1">
                Xem tất cả <ArrowRight className="w-3 h-3" />
              </Link>
            </div>
            <div className="space-y-3">
              {(leaderboard as Array<{ rank: number; full_name: string; bizcoins: number; department: string }>).map((entry, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                    entry.rank === 1 ? "bg-amber-400 text-white" :
                    entry.rank === 2 ? "bg-gray-300 text-white" :
                    entry.rank === 3 ? "bg-orange-400 text-white" :
                    "bg-gray-100 text-gray-600"
                  }`}>
                    {entry.rank === 1 ? "🥇" : entry.rank === 2 ? "🥈" : entry.rank === 3 ? "🥉" : entry.rank}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-gray-800 truncate">{entry.full_name}</p>
                    <p className="text-xs text-gray-400">{DEPARTMENT_LABELS[entry.department] || entry.department}</p>
                  </div>
                  <span className="text-sm font-bold text-amber-600">
                    {formatCoins(entry.bizcoins)}
                  </span>
                </div>
              ))}
            </div>

            {/* Badges */}
            {(stats.badges as Array<{ icon: string; name: string; color: string }>)?.length > 0 && (
              <div className="mt-6">
                <p className="text-xs font-semibold text-gray-500 mb-2">Huy hiệu của bạn</p>
                <div className="flex flex-wrap gap-2">
                  {(stats.badges as Array<{ icon: string; name: string; color: string }>).map((badge, i) => (
                    <div
                      key={i}
                      className="flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium text-white"
                      style={{ background: badge.color }}
                      title={badge.name}
                    >
                      {badge.icon} {badge.name}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </AppShell>
  );
}
