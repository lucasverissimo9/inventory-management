import { MantineProvider } from "@mantine/core";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@mantine/core/styles.css";
import { AuthProvider } from "@/providers/AuthProvider";
import { AppRouter } from "@/routes";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <MantineProvider>
        <AuthProvider>
          <AppRouter />
        </AuthProvider>
      </MantineProvider>
    </QueryClientProvider>
  </StrictMode>
);