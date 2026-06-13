"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import AppShell from "@/components/layout/AppShell";
import { communityApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import { Send, Loader2 } from "lucide-react";
import { ZalopayLogo } from "@/components/ZalopayLogo";

interface Message {
  id: string;
  type: "system" | "user" | "assistant";
  sender_id: string | null;
  sender_name: string;
  content: string;
  is_broadcast: boolean;
  created_at: string;
}

function Avatar({ name, isBizgro }: { name: string; isBizgro?: boolean }) {
  if (isBizgro) {
    return (
      <div className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-600 to-green-500 flex items-center justify-center flex-shrink-0 shadow">
        <span className="text-white font-black text-xs">Z</span>
      </div>
    );
  }
  return (
    <div className="w-9 h-9 rounded-full bg-violet-500 flex items-center justify-center flex-shrink-0 shadow">
      <span className="text-white font-bold text-sm">{name.charAt(0).toUpperCase()}</span>
    </div>
  );
}

function MessageBubble({ msg, currentEmployeeId }: { msg: Message; currentEmployeeId: string }) {
  const isMine = msg.type === "user" && msg.sender_id === currentEmployeeId;
  const isBizgro = msg.type === "system" || msg.type === "assistant";
  const time = new Date(msg.created_at).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });

  if (isMine) {
    return (
      <div className="flex justify-end gap-2 items-end">
        <div className="max-w-xs lg:max-w-md">
          <div className="bg-violet-600 text-white rounded-2xl rounded-br-sm px-4 py-2.5 shadow">
            <p className="text-sm leading-relaxed">{msg.content}</p>
          </div>
          <p className="text-xs text-gray-400 mt-1 text-right">{time}</p>
        </div>
        <Avatar name={msg.sender_name} />
      </div>
    );
  }

  if (msg.type === "system") {
    return (
      <div className="flex justify-center">
        <div className="bg-gradient-to-r from-blue-50 to-green-50 border border-blue-100 rounded-2xl px-5 py-3 max-w-lg shadow-sm">
          <div className="flex items-center gap-2 mb-1">
            <Avatar isBizgro />
            <span className="text-xs font-bold text-blue-700">BizGro</span>
            <span className="text-xs text-gray-400">{time}</span>
          </div>
          <p className="text-sm text-gray-700 leading-relaxed">{msg.content}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-2 items-end">
      <Avatar isBizgro />
      <div className="max-w-xs lg:max-w-md">
        <p className="text-xs font-semibold text-blue-700 mb-1 ml-1">BizGro</p>
        <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-sm px-4 py-2.5 shadow-sm">
          <p className="text-sm text-gray-800 leading-relaxed">{msg.content}</p>
        </div>
        <p className="text-xs text-gray-400 mt-1 ml-1">{time}</p>
      </div>
    </div>
  );
}

export default function CommunityPage() {
  const { employee } = useAppStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [loading, setLoading] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetchFeed = useCallback(async () => {
    try {
      const res = await communityApi.feed();
      setMessages(res.data);
    } catch {
      // silent
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchFeed();
    pollingRef.current = setInterval(fetchFeed, 5000);
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [fetchFeed]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || sending) return;
    setInput("");
    setSending(true);
    try {
      const res = await communityApi.chat(text);
      setMessages((prev) => [...prev, res.data.user_message, res.data.ai_message]);
    } catch {
      // silent
    } finally {
      setSending(false);
    }
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <AppShell>
      <div className="flex flex-col h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-100 px-6 py-4 flex items-center gap-3 shadow-sm flex-shrink-0">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-green-500 flex items-center justify-center shadow">
            <span className="text-white font-black text-base">Z</span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <ZalopayLogo size="sm" />
              <span className="text-sm font-semibold text-gray-700">Community</span>
            </div>
            <p className="text-xs text-gray-400">Hỏi về điểm, hot trends, phần thưởng...</p>
          </div>
          <div className="ml-auto flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-xs text-gray-500">BizGro AI đang online</span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
          {loading ? (
            <div className="flex justify-center py-20">
              <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
            </div>
          ) : messages.length === 0 ? (
            <div className="text-center py-20 text-gray-400">
              <p className="text-lg mb-2">👋</p>
              <p className="text-sm">Chào {employee?.full_name}! Hỏi gì đó đi nào.</p>
            </div>
          ) : (
            messages.map((msg) => (
              <MessageBubble
                key={msg.id}
                msg={msg}
                currentEmployeeId={employee?.id || ""}
              />
            ))
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="bg-white border-t border-gray-100 px-4 py-3 flex-shrink-0">
          <div className="flex gap-3 items-end max-w-3xl mx-auto">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Hỏi về điểm BizCoin, hot trends, phần thưởng... (Enter để gửi)"
              rows={1}
              className="flex-1 resize-none rounded-2xl border border-gray-200 px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent bg-gray-50 leading-relaxed"
              style={{ maxHeight: 120 }}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || sending}
              className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-green-500 flex items-center justify-center shadow hover:opacity-90 disabled:opacity-40 transition-all flex-shrink-0"
            >
              {sending ? (
                <Loader2 className="w-4 h-4 text-white animate-spin" />
              ) : (
                <Send className="w-4 h-4 text-white" />
              )}
            </button>
          </div>
          <p className="text-xs text-gray-400 text-center mt-2">
            Shift+Enter để xuống dòng
          </p>
        </div>
      </div>
    </AppShell>
  );
}
