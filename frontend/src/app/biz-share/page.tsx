"use client";
import { useEffect, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { bizShareApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import toast from "react-hot-toast";
import { Share2, Copy, ExternalLink, Zap, Facebook, Linkedin } from "lucide-react";
import { cn, formatDate } from "@/lib/utils";
import { MarkdownText } from "@/components/shared/MarkdownText";

interface Campaign {
  id: string;
  title: string;
  product_name: string;
  description: string;
  reward_coins: number;
  commission_rate: number;
  image_url: string;
}

interface GeneratedPost {
  id: string;
  style: string;
  content: string;
  hashtags: string[];
  affiliate_code: string;
  platform: string;
}

const PLATFORMS = [
  { id: "facebook", label: "Facebook", icon: "📘", desc: "Thân thiện, cá nhân" },
  { id: "linkedin", label: "LinkedIn", icon: "💼", desc: "Chuyên nghiệp, B2B" },
  { id: "tiktok", label: "TikTok", icon: "🎵", desc: "Vui nhộn, viral" },
];

export default function BizSharePage() {
  const { employee, updateCoins } = useAppStore();
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null);
  const [selectedPlatform, setSelectedPlatform] = useState("facebook");
  const [generating, setGenerating] = useState(false);
  const [generatedPosts, setGeneratedPosts] = useState<GeneratedPost[]>([]);
  const [affiliateCode, setAffiliateCode] = useState("");
  const [selectedPostId, setSelectedPostId] = useState<string | null>(null);
  const [sharing, setSharing] = useState(false);
  const [myPosts, setMyPosts] = useState<unknown[]>([]);
  const [tab, setTab] = useState<"generate" | "history">("generate");
  const [loadingCampaigns, setLoadingCampaigns] = useState(true);

  useEffect(() => {
    setLoadingCampaigns(true);
    bizShareApi.campaigns()
      .then((r: { data: Campaign[] }) => {
        setCampaigns(r.data);
        if (r.data.length > 0) setSelectedCampaign(r.data[0]);
      })
      .catch(() => toast.error("Không tải được danh sách chiến dịch"))
      .finally(() => setLoadingCampaigns(false));
    bizShareApi.myPosts().then(r => setMyPosts(r.data)).catch(() => {});
  }, []);

  const handleGenerate = async () => {
    if (!selectedCampaign) return toast.error("Vui lòng chọn chiến dịch");
    setGenerating(true);
    setGeneratedPosts([]);
    try {
      const res = await bizShareApi.generateContent({
        campaign_id: selectedCampaign.id,
        platform: selectedPlatform,
      });
      setGeneratedPosts(res.data.posts);
      setAffiliateCode(res.data.affiliate_code);
      toast.success(`Đã tạo ${res.data.posts.length} bài viết AI!`);
    } catch {
      toast.error("Lỗi tạo nội dung. Vui lòng thử lại.");
    }
    setGenerating(false);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success("Đã copy vào clipboard!");
  };

  const handleShare = async (postId: string) => {
    setSharing(true);
    try {
      const res = await bizShareApi.sharePost(postId, `https://zalopay.vn/ref/${affiliateCode}`);
      updateCoins(res.data.coins_earned);
      toast.success(`🎉 Đã chia sẻ! +${res.data.coins_earned} BizCoins`);
      bizShareApi.myPosts().then(r => setMyPosts(r.data));
    } catch {
      toast.error("Lỗi khi đánh dấu chia sẻ");
    }
    setSharing(false);
  };

  return (
    <AppShell>
      <div className="p-8 max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl gradient-bizshare flex items-center justify-center">
              <Share2 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">BIZ-SHARE</h1>
              <p className="text-sm text-gray-500">AI Social Selling Hub</p>
            </div>
          </div>
          <p className="text-gray-600 ml-13">
            Chọn chiến dịch → AI tạo nội dung → Chia sẻ kiếm BizCoins
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-gray-200">
          {[
            { id: "generate", label: "Tạo bài viết mới" },
            { id: "history", label: `Lịch sử (${myPosts.length})` },
          ].map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id as "generate" | "history")}
              className={cn(
                "px-4 py-2 text-sm font-medium border-b-2 transition-colors",
                tab === t.id
                  ? "border-pink-500 text-pink-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              )}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "generate" ? (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            {/* Left: Configuration */}
            <div className="lg:col-span-2 space-y-6">
              {/* Campaign selection */}
              <div className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-pink-500 text-white text-xs flex items-center justify-center">1</span>
                  Chọn chiến dịch
                </h3>
                <div className="space-y-2">
                  {loadingCampaigns ? (
                    <div className="flex items-center justify-center py-6 text-gray-400">
                      <div className="w-5 h-5 border-2 border-pink-400 border-t-transparent rounded-full animate-spin mr-2" />
                      <span className="text-sm">Đang tải chiến dịch...</span>
                    </div>
                  ) : campaigns.length === 0 ? (
                    <p className="text-sm text-gray-400 text-center py-4">Không có chiến dịch nào</p>
                  ) : null}
                  {campaigns.map(c => (
                    <button
                      key={c.id}
                      onClick={() => setSelectedCampaign(c)}
                      className={cn(
                        "w-full text-left p-3 rounded-xl border-2 transition-all",
                        selectedCampaign?.id === c.id
                          ? "border-pink-400 bg-pink-50"
                          : "border-gray-100 hover:border-gray-200"
                      )}
                    >
                      <p className="font-semibold text-sm text-gray-800">{c.title}</p>
                      <p className="text-xs text-gray-500 mt-1 line-clamp-2">{c.description}</p>
                      <div className="flex gap-2 mt-2">
                        <span className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">
                          +{c.reward_coins} coins
                        </span>
                        <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">
                          {c.commission_rate}% hoa hồng
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Platform selection */}
              <div className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
                <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-pink-500 text-white text-xs flex items-center justify-center">2</span>
                  Nền tảng đăng bài
                </h3>
                <div className="grid grid-cols-3 gap-2">
                  {PLATFORMS.map(p => (
                    <button
                      key={p.id}
                      onClick={() => setSelectedPlatform(p.id)}
                      className={cn(
                        "p-3 rounded-xl border-2 text-center transition-all",
                        selectedPlatform === p.id
                          ? "border-pink-400 bg-pink-50"
                          : "border-gray-100 hover:border-gray-200"
                      )}
                    >
                      <div className="text-2xl mb-1">{p.icon}</div>
                      <p className="text-xs font-semibold text-gray-800">{p.label}</p>
                      <p className="text-xs text-gray-400">{p.desc}</p>
                    </button>
                  ))}
                </div>
              </div>

              <button
                onClick={handleGenerate}
                disabled={!selectedCampaign || generating}
                className="w-full gradient-bizshare text-white py-4 rounded-2xl font-bold text-sm hover:opacity-90 disabled:opacity-50 transition-all shadow-lg flex items-center justify-center gap-2"
              >
                {generating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    AI đang tạo nội dung...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    Tạo nội dung AI
                  </>
                )}
              </button>
            </div>

            {/* Right: Generated posts */}
            <div className="lg:col-span-3">
              {generatedPosts.length === 0 ? (
                <div className="bg-white rounded-2xl p-12 shadow-sm border border-gray-100 text-center">
                  <div className="text-6xl mb-4">✨</div>
                  <h3 className="font-semibold text-gray-600">Chờ AI tạo nội dung</h3>
                  <p className="text-sm text-gray-400 mt-2">
                    Chọn chiến dịch và nền tảng, sau đó bấm "Tạo nội dung AI"
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {affiliateCode && (
                    <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-amber-800">Mã affiliate của bạn</p>
                        <p className="text-lg font-bold text-amber-600 font-mono">{affiliateCode}</p>
                      </div>
                      <button
                        onClick={() => copyToClipboard(affiliateCode)}
                        className="p-2 rounded-xl bg-amber-100 hover:bg-amber-200 transition-colors"
                      >
                        <Copy className="w-4 h-4 text-amber-700" />
                      </button>
                    </div>
                  )}

                  {generatedPosts.map((post, i) => (
                    <div
                      key={post.id}
                      className={cn(
                        "bg-white rounded-2xl p-5 shadow-sm border-2 transition-all cursor-pointer",
                        selectedPostId === post.id ? "border-pink-400" : "border-gray-100 hover:border-gray-200"
                      )}
                      onClick={() => setSelectedPostId(post.id)}
                    >
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-semibold px-2 py-1 rounded-full bg-pink-100 text-pink-700 capitalize">
                          {post.style}
                        </span>
                        <div className="flex gap-2">
                          <button
                            onClick={(e) => { e.stopPropagation(); copyToClipboard(post.content); }}
                            className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                          >
                            <Copy className="w-3.5 h-3.5 text-gray-400" />
                          </button>
                        </div>
                      </div>
                      <MarkdownText text={post.content} className="text-sm text-gray-700" />
                      {post.hashtags?.length > 0 && (
                        <p className="text-xs text-blue-500 mt-2">{post.hashtags.join(" ")}</p>
                      )}
                      <div className="mt-4 flex gap-2">
                        <button
                          onClick={(e) => { e.stopPropagation(); handleShare(post.id); }}
                          disabled={sharing}
                          className="flex-1 gradient-bizshare text-white py-2 rounded-xl text-xs font-semibold hover:opacity-90 disabled:opacity-50 flex items-center justify-center gap-1"
                        >
                          <ExternalLink className="w-3 h-3" />
                          Đã chia sẻ (+{selectedCampaign?.reward_coins || 10} 🪙)
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          /* History tab */
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(myPosts as Array<{ id: string; platform: string; content: string; status: string; clicks: number; conversions: number; affiliate_code: string; shared_at?: string }>).length === 0 ? (
              <div className="col-span-2 text-center py-12 text-gray-400">
                <Share2 className="w-12 h-12 mx-auto mb-3 opacity-30" />
                <p>Chưa có bài viết nào. Hãy tạo và chia sẻ ngay!</p>
              </div>
            ) : (
              (myPosts as Array<{ id: string; platform: string; content: string; status: string; clicks: number; conversions: number; affiliate_code: string; shared_at?: string }>).map(post => (
                <div key={post.id} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold px-2 py-1 rounded-full bg-blue-100 text-blue-700 capitalize">
                      {post.platform}
                    </span>
                    <span className={cn(
                      "text-xs px-2 py-1 rounded-full font-medium",
                      post.status === "shared" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"
                    )}>
                      {post.status === "shared" ? "Đã đăng" : "Nháp"}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 line-clamp-3">{post.content}</p>
                  <div className="mt-3 flex items-center gap-4 text-xs text-gray-500">
                    <span>👆 {post.clicks} clicks</span>
                    <span>✅ {post.conversions} conversions</span>
                    <span className="font-mono text-violet-600">{post.affiliate_code}</span>
                  </div>
                  {post.shared_at && (
                    <p className="text-xs text-gray-400 mt-2">{formatDate(post.shared_at)}</p>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
