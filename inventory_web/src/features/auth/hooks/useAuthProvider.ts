import { useCallback, useEffect, useState } from "react";
import { tokenStore } from "@/api/client";
import { authApi } from "@/features/auth/api/authApi";
import type { AuthUser, LoginRequest, RegisterRequest } from "@/features/auth/types";

export const useAuthProvider = () => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true); 

  const login = useCallback(async (credentials: LoginRequest) => {
    const data = await authApi.login(credentials);
    tokenStore.set(data.access);
    setUser(data.user);
  }, []);

  const register = useCallback(async (payload: RegisterRequest) => {
    const data = await authApi.register(payload);
    tokenStore.set(data.access);
    setUser(data.user);
  }, []);

  const logout = useCallback(async () => {
    try { await authApi.logout(); } finally {
      tokenStore.clear();
      setUser(null);
      localStorage.removeItem("activeCompanyKey");
    }
  }, []);

  return { user, isAuthenticated: !!user, isLoading, login, register, logout };
};