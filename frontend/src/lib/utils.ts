import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCoins(n: number): string {
  return new Intl.NumberFormat("vi-VN").format(n);
}

export function formatDate(d: string | Date): string {
  return new Intl.DateTimeFormat("vi-VN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(d));
}

export const DEPARTMENT_LABELS: Record<string, string> = {
  tech: "Công nghệ",
  hr: "Nhân sự",
  sales: "Kinh doanh",
  marketing: "Marketing",
  operations: "Vận hành",
  finance: "Tài chính",
  product: "Sản phẩm",
};

export const STATUS_COLORS: Record<string, string> = {
  draft: "bg-gray-100 text-gray-700",
  shared: "bg-green-100 text-green-700",
  tracked: "bg-blue-100 text-blue-700",
  submitted: "bg-yellow-100 text-yellow-700",
  enhancing: "bg-purple-100 text-purple-700",
  enhanced: "bg-indigo-100 text-indigo-700",
  reviewing: "bg-orange-100 text-orange-700",
  approved: "bg-green-100 text-green-700",
  implementing: "bg-blue-100 text-blue-700",
  completed: "bg-teal-100 text-teal-700",
  rejected: "bg-red-100 text-red-700",
  matched: "bg-purple-100 text-purple-700",
  introduced: "bg-blue-100 text-blue-700",
  in_progress: "bg-yellow-100 text-yellow-700",
  closed_won: "bg-green-100 text-green-700",
  closed_lost: "bg-red-100 text-red-700",
};
