import { createContext, useContext, type ReactNode } from "react";
import { useAuthProvider } from "@/features/auth/hooks/useAuthProvider";
import type { AuthContextValue } from "@/features/auth/types";

const AuthContext = createContext<AuthContextValue | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const auth = useAuthProvider();
  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within <AuthProvider>");
  return context;
};