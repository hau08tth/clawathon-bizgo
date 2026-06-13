"use client";
import { useEffect, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { gamificationApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import toast from "react-hot-toast";
import { ShoppingBag, Coins } from "lucide-react";
import { cn, formatCoins } from "@/lib/utils";

interface StoreItem {
  id: string;
  name: string;
  description: string;
  image_url: string;
  cost: number;
  stock: number;
  category: string;
}

const CATEGORY_MAP: Record<string, { label: string; icon: string }> = {
  time_off: { label: "Ngày phép", icon: "🌴" },
  voucher: { label: "Voucher", icon: "🎟️" },
  learning: { label: "Học tập", icon: "📚" },
  tech: { label: "Công nghệ", icon: "💻" },
  wellness: { label: "Sức khỏe", icon: "🧘" },
  general: { label: "Tổng hợp", icon: "🎁" },
};

export default function BizStorePage() {
  const { employee, updateCoins } = useAppStore();
  const [items, setItems] = useState<StoreItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [redeeming, setRedeeming] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState("all");

  useEffect(() => {
    gamificationApi.store().then(r => {
      setItems(r.data);
      setLoading(false);
    });
  }, []);

  const handleRedeem = async (item: StoreItem) => {
    if ((employee?.bizcoins || 0) < item.cost) {
      toast.error(`Không đủ BizCoins. Cần thêm ${formatCoins(item.cost - (employee?.bizcoins || 0))} coins`);
      return;
    }
    setRedeeming(item.id);
    try {
      const res = await gamificationApi.redeem(item.id);
      updateCoins(-item.cost);
      toast.success(`🎉 ${res.data.message}`);
      gamificationApi.store().then(r => setItems(r.data));
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail || "Lỗi đổi quà");
    }
    setRedeeming(null);
  };

  const categories = ["all", ...Object.keys(CATEGORY_MAP)];
  const filteredItems = activeCategory === "all"
    ? items
    : items.filter(i => i.category === activeCategory);

  if (loading) return (
    <AppShell>
      <div className="flex items-center justify-center h-screen">
        <div className="w-12 h-12 border-4 border-violet-300 border-t-violet-600 rounded-full animate-spin" />
      </div>
    </AppShell>
  );

  return (
    <AppShell>
      <div className="p-8 max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-xl gradient-bizgro flex items-center justify-center">
                <ShoppingBag className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">BizStore</h1>
                <p className="text-sm text-gray-500">Chợ đổi quà BizCoins</p>
              </div>
            </div>
            <p className="text-gray-600">Dùng BizCoins tích lũy để đổi các phần thưởng hấp dẫn</p>
          </div>
          {/* Coin balance */}
          <div className="bg-amber-50 border border-amber-200 rounded-2xl px-6 py-4 text-center">
            <p className="text-xs text-amber-600 font-medium">BizCoins của bạn</p>
            <div className="flex items-center gap-2">
              <span className="text-2xl">🪙</span>
              <span className="text-2xl font-black text-amber-600">{formatCoins(employee?.bizcoins || 0)}</span>
            </div>
          </div>
        </div>

        {/* Category filter */}
        <div className="flex gap-2 flex-wrap mb-6">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={cn(
                "px-4 py-2 rounded-xl text-sm font-medium transition-all",
                activeCategory === cat
                  ? "gradient-bizgro text-white shadow-md"
                  : "bg-white text-gray-600 hover:bg-gray-50 border border-gray-200"
              )}
            >
              {cat === "all" ? "🛍️ Tất cả" : `${CATEGORY_MAP[cat]?.icon} ${CATEGORY_MAP[cat]?.label}`}
            </button>
          ))}
        </div>

        {/* Items grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredItems.map(item => {
            const canAfford = (employee?.bizcoins || 0) >= item.cost;
            const outOfStock = item.stock === 0;
            return (
              <div
                key={item.id}
                className={cn(
                  "bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden card-hover",
                  !canAfford && "opacity-80"
                )}
              >
                <div className="aspect-video bg-gray-50 flex items-center justify-center text-6xl">
                  {CATEGORY_MAP[item.category]?.icon || "🎁"}
                </div>
                <div className="p-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-bold text-gray-800 text-sm">{item.name}</h3>
                    {item.stock > 0 && item.stock <= 5 && (
                      <span className="text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full whitespace-nowrap">
                        Còn {item.stock}
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-gray-500 mb-4 line-clamp-2">{item.description}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1">
                      <span className="text-lg">🪙</span>
                      <span className="font-black text-amber-600">{formatCoins(item.cost)}</span>
                    </div>
                    <button
                      onClick={() => handleRedeem(item)}
                      disabled={!canAfford || outOfStock || redeeming === item.id}
                      className={cn(
                        "px-4 py-2 rounded-xl text-xs font-bold transition-all",
                        outOfStock
                          ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                          : canAfford
                          ? "gradient-bizgro text-white hover:opacity-90 shadow-md"
                          : "bg-gray-100 text-gray-400 cursor-not-allowed"
                      )}
                    >
                      {redeeming === item.id ? "..." :
                        outOfStock ? "Hết hàng" :
                        !canAfford ? `Thiếu ${formatCoins(item.cost - (employee?.bizcoins || 0))}` :
                        "Đổi ngay"}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AppShell>
  );
}
