"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppStore } from "@/lib/store";
import Sidebar from "./Sidebar";

export default function AppShell({ children }: { children: React.ReactNode }) {
  const { token } = useAppStore();
  const router = useRouter();

  useEffect(() => {
    if (!token) router.push("/login");
  }, [token, router]);

  if (!token) return null;

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
}
