import { useMutation } from "@tanstack/react-query";
import { useAuth } from "@/providers/AuthProvider";
import type { LoginRequest } from "@/features/auth/types";

export const useLogin = () => {
  const { login } = useAuth();

  return useMutation({
    mutationFn: (credentials: LoginRequest) => login(credentials),
  });
};