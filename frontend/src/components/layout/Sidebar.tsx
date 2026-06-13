"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { cn, formatCoins } from "@/lib/utils";
import { useAppStore } from "@/lib/store";
import {
  Share2, Network, Lightbulb, Trophy, ShoppingBag,
  LogOut, Coins, User, Rocket, ChevronRight
} from "lucide-react";

const NAV_ITEMS = [
  {
    label: "BIZ-SHARE",
    sublabel: "AI Social Selling",
    href: "/biz-share",
    icon: Share2,
    gradient: "gradient-bizshare",
    color: "text-pink-600",
    bg: "bg-pink-50 hover:bg-pink-100",
    activeBg: "bg-pink-100 border-l-4 border-pink-500",
  },
  {
    label: "BIZ-CONNECT",
    sublabel: "AI Referral Matcher",
    href: "/biz-connect",
    icon: Network,
    gradient: "gradient-bizconnect",
    color: "text-cyan-600",
    bg: "bg-cyan-50 hover:bg-cyan-100",
    activeBg: "bg-cyan-100 border-l-4 border-cyan-500",
  },
  {
    label: "BIZ-COCREATE",
    sublabel: "AI Idea Incubator",
    href: "/biz-cocreate",
    icon: Lightbulb,
    gradient: "gradient-bizcocreate",
    color: "text-emerald-600",
    bg: "bg-emerald-50 hover:bg-emerald-100",
    activeBg: "bg-emerald-100 border-l-4 border-emerald-500",
  },
  {
    label: "Leaderboard",
    sublabel: "Bảng xếp hạng",
    href: "/leaderboard",
    icon: Trophy,
    gradient: "gradient-gold",
    color: "text-amber-600",
    bg: "bg-amber-50 hover:bg-amber-100",
    activeBg: "bg-amber-100 border-l-4 border-amber-500",
  },
  {
    label: "BizStore",
    sublabel: "Chợ đổi quà",
    href: "/bizstore",
    icon: ShoppingBag,
    gradient: "gradient-bizgro",
    color: "text-violet-600",
    bg: "bg-violet-50 hover:bg-violet-100",
    activeBg: "bg-violet-100 border-l-4 border-violet-500",
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { employee, logout } = useAppStore();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <aside className="w-72 min-h-screen bg-white border-r border-gray-100 flex flex-col shadow-sm">
      {/* Logo */}
      <div className="p-6 border-b border-gray-100">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl gradient-bizgro flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform">
            <Rocket className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">
              BizGro
            </h1>
            <p className="text-xs text-gray-400">Business Growth from Within</p>
          </div>
        </Link>
      </div>

      {/* User profile */}
      {employee && (
        <div className="p-4 mx-3 mt-4 rounded-2xl bg-gradient-to-r from-violet-50 to-purple-50 border border-violet-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full gradient-bizgro flex items-center justify-center text-white font-bold text-sm">
              {employee.full_name.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-gray-800 truncate">{employee.full_name}</p>
              <p className="text-xs text-gray-500 truncate">{employee.position || employee.department}</p>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2 bg-white rounded-xl px-3 py-2 shadow-sm">
            <div className="w-5 h-5 rounded-full bg-amber-400 flex items-center justify-center">
              <span className="text-xs">🪙</span>
            </div>
            <span className="text-sm font-bold text-amber-600">
              {formatCoins(employee.bizcoins)}
            </span>
            <span className="text-xs text-gray-400">BizCoins</span>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 mt-4">
        <p className="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Modules
        </p>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-150 group",
                isActive ? item.activeBg : item.bg
              )}
            >
              <div className={cn(
                "w-8 h-8 rounded-lg flex items-center justify-center",
                isActive ? item.gradient : "bg-gray-100 group-hover:bg-gray-200"
              )}>
                <Icon className={cn("w-4 h-4", isActive ? "text-white" : item.color)} />
              </div>
              <div className="flex-1">
                <p className={cn("text-sm font-semibold", isActive ? "text-gray-900" : "text-gray-600")}>
                  {item.label}
                </p>
                <p className="text-xs text-gray-400">{item.sublabel}</p>
              </div>
              {isActive && <ChevronRight className="w-4 h-4 text-gray-400" />}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-3 border-t border-gray-100 space-y-1">
        <Link
          href="/profile"
          className="flex items-center gap-3 px-3 py-2 rounded-xl text-gray-600 hover:bg-gray-50 transition-colors"
        >
          <User className="w-4 h-4" />
          <span className="text-sm">Hồ sơ</span>
        </Link>
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-red-500 hover:bg-red-50 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span className="text-sm">Đăng xuất</span>
        </button>
      </div>
    </aside>
  );
}
