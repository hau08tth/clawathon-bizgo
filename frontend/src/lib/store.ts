import { create } from "zustand";

interface Employee {
  id: string;
  email: string;
  full_name: string;
  department: string;
  position: string;
  social_style: string;
  bizcoins: number;
  avatar_url?: string;
  is_admin: boolean;
}

interface AppState {
  employee: Employee | null;
  token: string | null;
  setEmployee: (employee: Employee) => void;
  setToken: (token: string) => void;
  logout: () => void;
  updateCoins: (amount: number) => void;
}

export const useAppStore = create<AppState>((set) => ({
  employee: typeof window !== "undefined"
    ? JSON.parse(localStorage.getItem("bizgro_employee") || "null")
    : null,
  token: typeof window !== "undefined"
    ? localStorage.getItem("bizgro_token")
    : null,

  setEmployee: (employee) => {
    localStorage.setItem("bizgro_employee", JSON.stringify(employee));
    set({ employee });
  },

  setToken: (token) => {
    localStorage.setItem("bizgro_token", token);
    set({ token });
  },

  logout: () => {
    localStorage.removeItem("bizgro_token");
    localStorage.removeItem("bizgro_employee");
    set({ employee: null, token: null });
  },

  updateCoins: (amount) =>
    set((state) => ({
      employee: state.employee
        ? { ...state.employee, bizcoins: state.employee.bizcoins + amount }
        : null,
    })),
}));
