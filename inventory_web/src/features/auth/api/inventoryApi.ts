import { apiClient } from "@/api/client";
import type { AuthResponse, LoginRequest, RegisterRequest, AuthUser } from "@/features/auth/types";

export const authApi = {
  login: (data: LoginRequest) =>
    apiClient.post<AuthResponse>("/auth/login/", data).then((r) => r.data),

  register: (data: RegisterRequest) =>
    apiClient.post<AuthResponse>("/auth/register/", data).then((r) => r.data),

  refresh: () =>
    apiClient.post<AuthResponse>("/auth/refresh/").then((r) => r.data),

  logout: () =>
    apiClient.post("/auth/logout/"),
};