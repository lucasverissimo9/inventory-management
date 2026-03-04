import { lazy, Suspense } from "react";
import { createBrowserRouter, Navigate, Outlet, RouterProvider } from "react-router-dom";
import { LoadingOverlay } from "@mantine/core";
import { useAuth } from "@/providers/AuthProvider";

const LoginPage = lazy(() => import("@/pages/LoginPage"));
const DashboardPage = lazy(() => import("@/pages/DashboardPage"));

const ProtectedRoute = () => {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) return <LoadingOverlay visible />;
  return isAuthenticated ? <Outlet /> : <Navigate to="auth/login" replace />;
};

const PublicOnlyRoute = () => {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) return <LoadingOverlay visible />;
  return isAuthenticated ? <Navigate to="/dashboard" replace /> : <Outlet />;
};

const router = createBrowserRouter([
  {
    element: <PublicOnlyRoute />,
    children: [
      { path: "/login", element: <Suspense fallback={null}><LoginPage /></Suspense> },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      { path: "/dashboard", element: <Suspense fallback={null}><DashboardPage /></Suspense> },
    ],
  },
  { path: "*", element: <Navigate to="/dashboard" replace /> },
]);

export const AppRouter = () => <RouterProvider router={router} />;