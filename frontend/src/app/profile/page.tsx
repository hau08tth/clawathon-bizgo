"use client";
import { useEffect, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { gamificationApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import { formatCoins, formatDate, DEPARTMENT_LABELS } from "@/lib/utils";
import { User, Coins, Trophy, Star } from "lucide-react";

export default function ProfilePage() {
  const { employee } = useAppStore();
  const [stats, setStats] = useState<{
    bizcoins: number; rank: number; total_earned: number; total_spent: number;
    badges: Array<{ name: string; icon: string; color: string; awarded_at: string }>;
    recent_transactions: Array<{ type: string; amount: number; reason: string; created_at: string }>;
  } | null>(null);

  useEffect(() => {
    gamificationApi.myStats().then(r => setStats(r.data));
  }, []);

  return (
    <AppShell>
      <div className="p-8 max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Hồ sơ cá nhân</h1>

        {/* Profile card */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-6">
          <div className="flex items-center gap-4">
            <div className="w-20 h-20 rounded-full gradient-bizgro flex items-center justify-center text-white text-3xl font-bold shadow-lg">
              {employee?.full_name?.charAt(0)}
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">{employee?.full_name}</h2>
              <p className="text-gray-500">{employee?.position || "Employee"}</p>
              <p className="text-sm text-gray-400">{DEPARTMENT_LABELS[employee?.department || ""] || employee?.department}</p>
              <p className="text-sm text-gray-400">{employee?.email}</p>
            </div>
          </div>
        </div>

        {/* Stats */}
        {stats && (
          <>
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5 text-center">
                <p className="text-xs text-amber-600 font-medium">BizCoins hiện tại</p>
                <p className="text-3xl font-black text-amber-600 mt-1">🪙 {formatCoins(stats.bizcoins)}</p>
                <p className="text-xs text-gray-400 mt-1">Hạng #{stats.rank}</p>
              </div>
              <div className="bg-green-50 border border-green-200 rounded-2xl p-5 text-center">
                <p className="text-xs text-green-600 font-medium">Tổng đã kiếm</p>
                <p className="text-3xl font-black text-green-600 mt-1">+{formatCoins(stats.total_earned)}</p>
                <p className="text-xs text-gray-400 mt-1">Đã dùng: {formatCoins(stats.total_spent)}</p>
              </div>
            </div>

            {/* Badges */}
            {stats.badges?.length > 0 && (
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-6">
                <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <Star className="w-4 h-4 text-amber-400" /> Huy hiệu của tôi
                </h3>
                <div className="grid grid-cols-2 gap-3">
                  {stats.badges.map((badge, i) => (
                    <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-gray-50">
                      <div className="w-10 h-10 rounded-full flex items-center justify-center text-2xl" style={{ background: badge.color + "20" }}>
                        {badge.icon}
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-gray-800">{badge.name}</p>
                        <p className="text-xs text-gray-400">{formatDate(badge.awarded_at)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Transaction history */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
              <h3 className="font-bold text-gray-800 mb-4">Lịch sử giao dịch</h3>
              <div className="space-y-3">
                {stats.recent_transactions?.map((tx, i) => (
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
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}
