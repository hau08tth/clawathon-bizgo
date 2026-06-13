"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { authApi } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import { Rocket, Mail, Lock, Eye, EyeOff } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("demo@zalopay.vn");
  const [password, setPassword] = useState("demo123");
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [fullName, setFullName] = useState("");
  const { setToken, setEmployee } = useAppStore();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isRegister) {
        const res = await authApi.register({ email, password, full_name: fullName });
        setToken(res.data.access_token);
        setEmployee(res.data.employee);
      } else {
        const res = await authApi.login(email, password);
        setToken(res.data.access_token);
        setEmployee(res.data.employee);
      }
      toast.success("Chào mừng đến BizGro! 🚀");
      router.push("/");
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail || "Đăng nhập thất bại");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left panel */}
      <div className="hidden lg:flex lg:w-1/2 gradient-bizgro flex-col items-center justify-center p-12 text-white">
        <div className="max-w-md">
          <div className="flex items-center gap-4 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-white/20 flex items-center justify-center">
              <Rocket className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-black">BizGro</h1>
              <p className="text-white/70">Business Growth from Within</p>
            </div>
          </div>
          <h2 className="text-3xl font-bold mb-4">
            Khi mỗi nhân viên là một động cơ tăng trưởng
          </h2>
          <p className="text-white/80 text-lg leading-relaxed mb-8">
            Tận dụng AI để biến mọi nhân viên thành đại sứ bán hàng,
            nhà kết nối B2B và nhà sáng kiến sản phẩm.
          </p>
          <div className="grid grid-cols-3 gap-4">
            {[
              { icon: "📢", label: "BIZ-SHARE", desc: "Social Selling" },
              { icon: "🤝", label: "BIZ-CONNECT", desc: "Referral Matcher" },
              { icon: "💡", label: "BIZ-COCREATE", desc: "Idea Incubator" },
            ].map((m) => (
              <div key={m.label} className="bg-white/10 rounded-2xl p-4 text-center">
                <div className="text-2xl mb-2">{m.icon}</div>
                <p className="font-bold text-sm">{m.label}</p>
                <p className="text-xs text-white/60">{m.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right panel */}
      <div className="flex-1 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <div className="text-center mb-8">
              <div className="w-14 h-14 gradient-bizgro rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                <Rocket className="w-7 h-7 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">
                {isRegister ? "Tạo tài khoản" : "Đăng nhập BizGro"}
              </h2>
              <p className="text-gray-500 text-sm mt-1">
                {isRegister ? "Tham gia cộng đồng tăng trưởng" : "Chào mừng trở lại!"}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {isRegister && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Họ và tên</label>
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                    placeholder="Nguyễn Văn A"
                    required
                  />
                </div>
              )}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3.5 w-4 h-4 text-gray-400" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                    placeholder="email@zalopay.vn"
                    required
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3.5 w-4 h-4 text-gray-400" />
                  <input
                    type={showPass ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPass(!showPass)}
                    className="absolute right-3 top-3.5 text-gray-400 hover:text-gray-600"
                  >
                    {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full gradient-bizgro text-white py-3 rounded-xl font-semibold hover:opacity-90 disabled:opacity-50 transition-all shadow-lg hover:shadow-xl"
              >
                {loading ? "Đang xử lý..." : isRegister ? "Tạo tài khoản" : "Đăng nhập"}
              </button>
            </form>

            <div className="mt-6 p-4 bg-violet-50 rounded-xl">
              <p className="text-xs text-violet-600 font-medium text-center">Demo account</p>
              <p className="text-xs text-gray-500 text-center">demo@zalopay.vn / demo123</p>
            </div>

            <p className="text-center text-sm text-gray-500 mt-4">
              {isRegister ? "Đã có tài khoản? " : "Chưa có tài khoản? "}
              <button
                onClick={() => setIsRegister(!isRegister)}
                className="text-violet-600 font-semibold hover:underline"
              >
                {isRegister ? "Đăng nhập" : "Đăng ký ngay"}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
