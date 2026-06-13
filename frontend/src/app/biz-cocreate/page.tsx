"use client";
import { useEffect, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { bizCoCreateApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import toast from "react-hot-toast";
import { Lightbulb, Zap, ChevronDown, ChevronUp, TrendingUp, BarChart3 } from "lucide-react";
import { cn, formatDate } from "@/lib/utils";

interface Idea {
  id: string;
  title: string;
  raw_idea: string;
  enhanced_proposal?: string;
  market_analysis?: string;
  feasibility_score?: number;
  cost_score?: number;
  revenue_potential_score?: number;
  total_score?: number;
  status: string;
  created_at: string;
  updated_at: string;
}

const STATUS_MAP: Record<string, { label: string; color: string; icon: string }> = {
  submitted: { label: "Đã gửi", color: "bg-gray-100 text-gray-600", icon: "📝" },
  enhancing: { label: "AI đang phân tích...", color: "bg-purple-100 text-purple-700", icon: "⚙️" },
  enhanced: { label: "Đã tăng cường", color: "bg-indigo-100 text-indigo-700", icon: "✨" },
  reviewing: { label: "Đang xem xét", color: "bg-yellow-100 text-yellow-700", icon: "👀" },
  approved: { label: "Được duyệt!", color: "bg-green-100 text-green-700", icon: "✅" },
  implementing: { label: "Đang triển khai", color: "bg-blue-100 text-blue-700", icon: "🚀" },
  completed: { label: "Hoàn thành", color: "bg-teal-100 text-teal-700", icon: "🎉" },
  rejected: { label: "Không phù hợp", color: "bg-red-100 text-red-700", icon: "❌" },
};

function ScoreBar({ label, value }: { label: string; value: number }) {
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-xs text-gray-600">{label}</span>
        <span className="text-xs font-bold text-gray-800">{value.toFixed(1)}/10</span>
      </div>
      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-emerald-400 to-teal-400 transition-all duration-500"
          style={{ width: `${(value / 10) * 100}%` }}
        />
      </div>
    </div>
  );
}

export default function BizCoCreatePage() {
  const { updateCoins } = useAppStore();
  const [title, setTitle] = useState("");
  const [rawIdea, setRawIdea] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [tab, setTab] = useState<"new" | "myideas" | "all">("new");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    bizCoCreateApi.myIdeas().then(r => setIdeas(r.data));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !rawIdea.trim()) return toast.error("Vui lòng nhập đủ thông tin");
    setSubmitting(true);
    try {
      const res = await bizCoCreateApi.submitIdea(title, rawIdea);
      const idea = res.data;
      if (idea.status === "approved") {
        updateCoins(500);
        toast.success("🎉 Ý tưởng được duyệt! +500 BizCoins");
      } else {
        toast.success("✨ Ý tưởng đã được AI phân tích!");
      }
      setTitle("");
      setRawIdea("");
      bizCoCreateApi.myIdeas().then(r => setIdeas(r.data));
      setTab("myideas");
    } catch {
      toast.error("Lỗi gửi ý tưởng. Vui lòng thử lại.");
    }
    setSubmitting(false);
  };

  return (
    <AppShell>
      <div className="p-8 max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl gradient-bizcocreate flex items-center justify-center">
              <Lightbulb className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">BIZ-COCREATE</h1>
              <p className="text-sm text-gray-500">AI Idea Incubator</p>
            </div>
          </div>
          <p className="text-gray-600">
            Chia sẻ ý tưởng thô → AI biến thành Business Proposal hoàn chỉnh → Gửi lên Ban GĐ
          </p>
        </div>

        {/* Reward info */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          {[
            { icon: "📝", label: "Gửi ý tưởng", coins: "+0", desc: "Miễn phí, không giới hạn" },
            { icon: "✅", label: "Ý tưởng được duyệt", coins: "+500", desc: "BizCoins thưởng" },
            { icon: "🚀", label: "Ý tưởng triển khai", coins: "+2000", desc: "BizCoins đặc biệt" },
          ].map(item => (
            <div key={item.label} className="bg-emerald-50 border border-emerald-100 rounded-2xl p-4 text-center">
              <div className="text-2xl mb-1">{item.icon}</div>
              <p className="text-xs text-gray-600">{item.label}</p>
              <p className="text-lg font-black text-emerald-600">{item.coins}</p>
              <p className="text-xs text-gray-400">{item.desc}</p>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-gray-200">
          {[
            { id: "new", label: "Gửi ý tưởng mới" },
            { id: "myideas", label: `Ý tưởng của tôi (${ideas.length})` },
          ].map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id as "new" | "myideas" | "all")}
              className={cn(
                "px-4 py-2 text-sm font-medium border-b-2 transition-colors",
                tab === t.id ? "border-emerald-500 text-emerald-600" : "border-transparent text-gray-500 hover:text-gray-700"
              )}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "new" ? (
          <form onSubmit={handleSubmit} className="space-y-4 max-w-3xl">
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
              <h3 className="font-semibold text-gray-800 mb-4">Ý tưởng của bạn</h3>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-1 block">Tiêu đề ý tưởng *</label>
                  <input
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                    placeholder="VD: Tối ưu UX thanh toán để tăng tỷ lệ chuyển đổi"
                    required
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-1 block">
                    Mô tả ý tưởng của bạn *
                  </label>
                  <textarea
                    value={rawIdea}
                    onChange={e => setRawIdea(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-none"
                    rows={5}
                    placeholder="Ví dụ: Em thấy bước xác nhận thanh toán trên app mình có quá nhiều bước, khách hàng hay bỏ giữa chừng. Nếu mình đơn giản hóa flow xuống còn 2 bước thì tỷ lệ hoàn thành giao dịch sẽ tăng đáng kể..."
                    required
                  />
                  <p className="text-xs text-gray-400 mt-1">{rawIdea.length} ký tự • Không cần viết hoa hết - AI sẽ hoàn thiện</p>
                </div>
              </div>
            </div>

            <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
              <p className="text-sm text-emerald-800 font-semibold mb-1">✨ AI sẽ làm gì với ý tưởng của bạn?</p>
              <ul className="text-xs text-emerald-700 space-y-1">
                <li>• Phân tích thị trường và bổ sung số liệu thực tế</li>
                <li>• Tạo Business Proposal chuẩn format Ban GĐ</li>
                <li>• Dự phóng tăng trưởng Sales Volume</li>
                <li>• Đánh giá tính khả thi và chấm điểm tự động</li>
              </ul>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full gradient-bizcocreate text-white py-4 rounded-2xl font-bold text-sm hover:opacity-90 disabled:opacity-50 transition-all shadow-lg flex items-center justify-center gap-2"
            >
              {submitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  AI đang phân tích ý tưởng...
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4" /> Gửi ý tưởng & Nhờ AI tăng cường
                </>
              )}
            </button>
          </form>
        ) : (
          <div className="space-y-4">
            {ideas.length === 0 ? (
              <div className="text-center py-12 text-gray-400">
                <Lightbulb className="w-12 h-12 mx-auto mb-3 opacity-30" />
                <p>Chưa có ý tưởng nào. Hãy gửi ý tưởng đầu tiên!</p>
              </div>
            ) : (
              ideas.map(idea => (
                <div key={idea.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                  <div className="p-5">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-bold text-gray-800">{idea.title}</h3>
                      <span className={cn("text-xs px-3 py-1 rounded-full font-medium whitespace-nowrap ml-2", STATUS_MAP[idea.status]?.color)}>
                        {STATUS_MAP[idea.status]?.icon} {STATUS_MAP[idea.status]?.label}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-2">{idea.raw_idea}</p>
                    <p className="text-xs text-gray-400 mt-2">{formatDate(idea.created_at)}</p>

                    {/* Scores */}
                    {idea.total_score !== undefined && idea.total_score > 0 && (
                      <div className="mt-4 grid grid-cols-3 gap-4">
                        <div className="text-center bg-gray-50 rounded-xl p-3">
                          <p className="text-xs text-gray-500">Khả thi</p>
                          <p className="text-xl font-black text-emerald-600">{idea.feasibility_score?.toFixed(1)}</p>
                        </div>
                        <div className="text-center bg-gray-50 rounded-xl p-3">
                          <p className="text-xs text-gray-500">Chi phí</p>
                          <p className="text-xl font-black text-blue-600">{idea.cost_score?.toFixed(1)}</p>
                        </div>
                        <div className="text-center bg-gray-50 rounded-xl p-3">
                          <p className="text-xs text-gray-500">Doanh số</p>
                          <p className="text-xl font-black text-purple-600">{idea.revenue_potential_score?.toFixed(1)}</p>
                        </div>
                      </div>
                    )}

                    {/* Expand enhanced proposal */}
                    {idea.enhanced_proposal && (
                      <>
                        <button
                          onClick={() => setExpandedId(expandedId === idea.id ? null : idea.id)}
                          className="mt-3 flex items-center gap-1 text-xs text-emerald-600 hover:text-emerald-800 font-medium"
                        >
                          {expandedId === idea.id ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                          {expandedId === idea.id ? "Ẩn" : "Xem"} Business Proposal đầy đủ
                        </button>
                        {expandedId === idea.id && (
                          <div className="mt-3 space-y-4">
                            <div className="bg-emerald-50 rounded-2xl p-4">
                              <div className="flex items-center gap-2 mb-2">
                                <TrendingUp className="w-4 h-4 text-emerald-600" />
                                <p className="text-sm font-bold text-emerald-800">Business Proposal</p>
                              </div>
                              <p className="text-sm text-emerald-800 whitespace-pre-wrap leading-relaxed">
                                {idea.enhanced_proposal}
                              </p>
                            </div>
                            {idea.market_analysis && (
                              <div className="bg-blue-50 rounded-2xl p-4">
                                <div className="flex items-center gap-2 mb-2">
                                  <BarChart3 className="w-4 h-4 text-blue-600" />
                                  <p className="text-sm font-bold text-blue-800">Phân tích thị trường</p>
                                </div>
                                <p className="text-sm text-blue-800 whitespace-pre-wrap leading-relaxed">
                                  {idea.market_analysis}
                                </p>
                              </div>
                            )}
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
