import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "BizGro - Business Growth from Within",
  description: "Every Employee a Growth Engine - Khi mỗi nhân viên là một động cơ tăng trưởng",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body className={inter.className}>
        {children}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: { borderRadius: "12px", background: "#1e1b4b", color: "#fff" },
          }}
        />
      </body>
    </html>
  );
}
