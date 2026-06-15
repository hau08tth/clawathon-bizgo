import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

export const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("bizgro_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("bizgro_token");
      localStorage.removeItem("bizgro_employee");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

// Auth
export const authApi = {
  login: (email: string, password: string) =>
    api.post("/auth/token", new URLSearchParams({ username: email, password }), {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }),
  register: (data: Record<string, string>) => api.post("/auth/register", data),
  me: () => api.get("/auth/me"),
};

// BizShare
export const bizShareApi = {
  campaigns: () => api.get("/bizshare/campaigns"),
  generateContent: (data: Record<string, string>) => api.post("/bizshare/generate-content", data),
  sharePost: (postId: string, postUrl: string) =>
    api.post("/bizshare/share", { post_id: postId, post_url: postUrl }),
  myPosts: () => api.get("/bizshare/my-posts"),
};

// BizConnect
export const bizConnectApi = {
  matchContacts: (contacts: Record<string, string>[]) =>
    api.post("/bizconnect/match", { contacts }),
  opportunities: () => api.get("/bizconnect/opportunities"),
  updateOpportunity: (id: string, status: string) =>
    api.patch(`/bizconnect/opportunities/${id}`, { status }),
};

// BizCoCreate
export const bizCoCreateApi = {
  submitIdea: (title: string, rawIdea: string) =>
    api.post("/bizcocreate/ideas", { title, raw_idea: rawIdea }),
  myIdeas: () => api.get("/bizcocreate/ideas"),
  allIdeas: () => api.get("/bizcocreate/ideas/all"),
  getIdea: (id: string) => api.get(`/bizcocreate/ideas/${id}`),
};

// Gamification
export const gamificationApi = {
  leaderboard: () => api.get("/gamification/leaderboard"),
  myStats: () => api.get("/gamification/my-stats"),
  store: () => api.get("/gamification/store"),
  redeem: (itemId: string) => api.post("/gamification/redeem", { item_id: itemId }),
  badges: () => api.get("/gamification/badges"),
};

// Community Chat
export const communityApi = {
  feed: () => api.get("/community/feed"),
  chat: (message: string) => api.post("/community/chat", { message }),
  broadcast: (content: string) => api.post("/community/broadcast", { content }),
};
