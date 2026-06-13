"use client";
import { useEffect, useState } from "react";
import AppShell from "@/components/layout/AppShell";
import { bizConnectApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import toast from "react-hot-toast";
import { Network, Plus, X, Zap, Copy, ChevronDown, ChevronUp } from "lucide-react";
import { cn, formatDate } from "@/lib/utils";

interface Contact {
  name: string;
  company: string;
  position: string;
  email: string;
  relationship: string;
}

interface Opportunity {
  id: string;
  contact_name: string;
  contact_company: string;
  contact_position: string;
  match_score?: number;
  match_reason: string;
  ice_breaker: string;
  pitching_script: string;
  status: string;
  reward_coins: number;
  created_at: string;
}

const STATUS_MAP: Record<string, { label: string; color: string }> = {
  matched: { label: "Đã match", color: "bg-purple-100 text-purple-700" },
  introduced: { label: "Đã giới thiệu", color: "bg-blue-100 text-blue-700" },
  in_progress: { label: "Đang đàm phán", color: "bg-yellow-100 text-yellow-700" },
  closed_won: { label: "Chốt deal!", color: "bg-green-100 text-green-700" },
  closed_lost: { label: "Không thành", color: "bg-red-100 text-red-700" },
};

const RELATIONSHIP_TYPES = ["colleague", "classmate", "friend", "partner", "other"];

export default function BizConnectPage() {
  const { updateCoins } = useAppStore();
  const [contacts, setContacts] = useState<Contact[]>([
    { name: "", company: "", position: "", email: "", relationship: "colleague" }
  ]);
  const [matching, setMatching] = useState(false);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [tab, setTab] = useState<"upload" | "opportunities">("upload");

  useEffect(() => {
    bizConnectApi.opportunities().then(r => setOpportunities(r.data));
  }, []);

  const addContact = () => setContacts([...contacts, { name: "", company: "", position: "", email: "", relationship: "colleague" }]);
  const removeContact = (i: number) => setContacts(contacts.filter((_, idx) => idx !== i));
  const updateContact = (i: number, field: keyof Contact, value: string) => {
    const updated = [...contacts];
    updated[i] = { ...updated[i], [field]: value };
    setContacts(updated);
  };

  const handleMatch = async () => {
    const valid = contacts.filter(c => c.name && c.company);
    if (valid.length === 0) return toast.error("Thêm ít nhất 1 liên hệ có tên và công ty");
    setMatching(true);
    try {
      const res = await bizConnectApi.matchContacts(valid);
      toast.success(`🎯 Tìm thấy ${res.data.matches_found} cơ hội từ ${res.data.total_contacts} liên hệ!`);
      bizConnectApi.opportunities().then(r => setOpportunities(r.data));
      setTab("opportunities");
    } catch {
      toast.error("Lỗi phân tích. Vui lòng thử lại.");
    }
    setMatching(false);
  };

  const handleUpdateStatus = async (oppId: string, status: string) => {
    try {
      const res = await bizConnectApi.updateOpportunity(oppId, status);
      if (res.data.coins_earned > 0) {
        updateCoins(res.data.coins_earned);
        toast.success(`🎉 +${res.data.coins_earned} BizCoins!`);
      }
      bizConnectApi.opportunities().then(r => setOpportunities(r.data));
    } catch {
      toast.error("Lỗi cập nhật trạng thái");
    }
  };

  return (
    <AppShell>
      <div className="p-8 max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl gradient-bizconnect flex items-center justify-center">
              <Network className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">BIZ-CONNECT</h1>
              <p className="text-sm text-gray-500">AI Referral Matchmaker</p>
            </div>
          </div>
          <p className="text-gray-600">
            Nhập danh sách liên hệ → AI tìm cơ hội B2B → Nhận pitching script cá nhân hóa
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-gray-200">
          {[
            { id: "upload", label: "Nhập liên hệ" },
            { id: "opportunities", label: `Cơ hội (${opportunities.length})` },
          ].map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id as "upload" | "opportunities")}
              className={cn(
                "px-4 py-2 text-sm font-medium border-b-2 transition-colors",
                tab === t.id ? "border-cyan-500 text-cyan-600" : "border-transparent text-gray-500 hover:text-gray-700"
              )}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "upload" ? (
          <div className="space-y-4">
            <div className="bg-cyan-50 border border-cyan-200 rounded-2xl p-4">
              <p className="text-sm text-cyan-800 font-medium">
                💡 Thêm những người bạn biết đang làm ở các công ty khác.
                AI sẽ phân tích và tìm cơ hội giới thiệu ZaloPay phù hợp nhất.
              </p>
            </div>

            {contacts.map((contact, i) => (
              <div key={i} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm font-semibold text-gray-600">Liên hệ #{i + 1}</span>
                  {contacts.length > 1 && (
                    <button onClick={() => removeContact(i)} className="p-1 rounded-lg hover:bg-red-50 text-red-400 transition-colors">
                      <X className="w-4 h-4" />
                    </button>
                  )}
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Tên *</label>
                    <input
                      className="w-full px-3 py-2 text-sm rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-cyan-400"
                      placeholder="Nguyễn Văn A"
                      value={contact.name}
                      onChange={e => updateContact(i, "name", e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Công ty *</label>
                    <input
                      className="w-full px-3 py-2 text-sm rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-cyan-400"
                      placeholder="VNG Corp"
                      value={contact.company}
                      onChange={e => updateContact(i, "company", e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Chức vụ</label>
                    <input
                      className="w-full px-3 py-2 text-sm rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-cyan-400"
                      placeholder="CTO / Director"
                      value={contact.position}
                      onChange={e => updateContact(i, "position", e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500 mb-1 block">Mối quan hệ</label>
                    <select
                      className="w-full px-3 py-2 text-sm rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-cyan-400"
                      value={contact.relationship}
                      onChange={e => updateContact(i, "relationship", e.target.value)}
                    >
                      {RELATIONSHIP_TYPES.map(r => (
                        <option key={r} value={r}>
                          {{ colleague: "Đồng nghiệp cũ", classmate: "Bạn học", friend: "Bạn bè", partner: "Đối tác", other: "Khác" }[r]}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            ))}

            <div className="flex gap-3">
              <button
                onClick={addContact}
                className="flex items-center gap-2 px-4 py-2 rounded-xl border-2 border-dashed border-cyan-300 text-cyan-600 hover:bg-cyan-50 transition-colors text-sm font-medium"
              >
                <Plus className="w-4 h-4" /> Thêm liên hệ
              </button>
              <button
                onClick={handleMatch}
                disabled={matching}
                className="flex-1 gradient-bizconnect text-white py-3 rounded-xl font-bold text-sm hover:opacity-90 disabled:opacity-50 transition-all shadow-lg flex items-center justify-center gap-2"
              >
                {matching ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    AI đang phân tích...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" /> Phân tích AI & Tìm cơ hội
                  </>
                )}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {opportunities.length === 0 ? (
              <div className="text-center py-12 text-gray-400">
                <Network className="w-12 h-12 mx-auto mb-3 opacity-30" />
                <p>Chưa có cơ hội nào. Hãy nhập danh sách liên hệ!</p>
              </div>
            ) : (
              opportunities.map(opp => (
                <div key={opp.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                  <div className="p-5">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-bold text-gray-800">{opp.contact_name}</h3>
                        <p className="text-sm text-gray-500">{opp.contact_position} @ {opp.contact_company}</p>
                      </div>
                      <span className={cn("text-xs px-3 py-1 rounded-full font-medium", STATUS_MAP[opp.status]?.color)}>
                        {STATUS_MAP[opp.status]?.label}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mt-3 bg-gray-50 rounded-xl p-3">{opp.match_reason}</p>

                    {/* Ice-breaker */}
                    {opp.ice_breaker && (
                      <div className="mt-3 bg-cyan-50 rounded-xl p-3">
                        <div className="flex items-center justify-between mb-1">
                          <p className="text-xs font-semibold text-cyan-700">Ice-breaker message</p>
                          <button onClick={() => navigator.clipboard.writeText(opp.ice_breaker).then(() => toast.success("Copied!"))}>
                            <Copy className="w-3.5 h-3.5 text-cyan-500" />
                          </button>
                        </div>
                        <p className="text-sm text-cyan-800">{opp.ice_breaker}</p>
                      </div>
                    )}

                    {/* Expand/Collapse pitching script */}
                    {opp.pitching_script && (
                      <>
                        <button
                          onClick={() => setExpandedId(expandedId === opp.id ? null : opp.id)}
                          className="mt-3 flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700"
                        >
                          {expandedId === opp.id ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                          {expandedId === opp.id ? "Ẩn" : "Xem"} pitching script
                        </button>
                        {expandedId === opp.id && (
                          <div className="mt-2 bg-indigo-50 rounded-xl p-3">
                            <div className="flex items-center justify-between mb-1">
                              <p className="text-xs font-semibold text-indigo-700">Pitching Script</p>
                              <button onClick={() => navigator.clipboard.writeText(opp.pitching_script).then(() => toast.success("Copied!"))}>
                                <Copy className="w-3.5 h-3.5 text-indigo-500" />
                              </button>
                            </div>
                            <p className="text-sm text-indigo-800 whitespace-pre-wrap">{opp.pitching_script}</p>
                          </div>
                        )}
                      </>
                    )}

                    {/* Actions */}
                    <div className="mt-4 flex gap-2 flex-wrap">
                      {opp.status === "matched" && (
                        <button
                          onClick={() => handleUpdateStatus(opp.id, "introduced")}
                          className="px-3 py-1.5 text-xs font-semibold rounded-xl gradient-bizconnect text-white hover:opacity-90"
                        >
                          ✅ Đã giới thiệu (+200 🪙)
                        </button>
                      )}
                      {opp.status === "introduced" && (
                        <>
                          <button
                            onClick={() => handleUpdateStatus(opp.id, "in_progress")}
                            className="px-3 py-1.5 text-xs font-semibold rounded-xl bg-yellow-100 text-yellow-700 hover:bg-yellow-200"
                          >
                            📞 Đang đàm phán
                          </button>
                          <button
                            onClick={() => handleUpdateStatus(opp.id, "closed_won")}
                            className="px-3 py-1.5 text-xs font-semibold rounded-xl bg-green-100 text-green-700 hover:bg-green-200"
                          >
                            🎉 Chốt deal!
                          </button>
                        </>
                      )}
                    </div>
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
