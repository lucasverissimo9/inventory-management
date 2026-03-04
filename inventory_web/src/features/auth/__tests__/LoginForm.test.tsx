import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "@/features/auth/components/LoginForm";
import { MantineProvider } from "@mantine/core";
import { MemoryRouter } from "react-router-dom";

vi.mock("@/features/auth/hooks/useLogin", () => ({
  useLogin: vi.fn(),
}));

import { useLogin } from "@/features/auth/hooks/useLogin";

const Wrapper = ({ children }: { children: React.ReactNode }) => (
  <MemoryRouter><MantineProvider>{children}</MantineProvider></MemoryRouter>
);

describe("LoginForm", () => {
  const mockMutate = vi.fn();

  beforeEach(() => {
    vi.mocked(useLogin).mockReturnValue({
      mutate: mockMutate, isPending: false, error: null,
    } as any);
  });

  it("calls login with email and password on valid submit", async () => {
    const user = userEvent.setup();
    render(<LoginForm />, { wrapper: Wrapper });

    await user.type(screen.getByLabelText(/email/i), "user@test.com");
    await user.type(screen.getByLabelText(/password/i), "password123");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(mockMutate).toHaveBeenCalledWith(
        { email: "user@test.com", password: "password123" },
        expect.any(Object)
      );
    });
  });

  it("shows error for invalid email without calling login", async () => {
    const user = userEvent.setup();
    render(<LoginForm />, { wrapper: Wrapper });

    await user.type(screen.getByLabelText(/email/i), "bademail");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByText(/valid email/i)).toBeInTheDocument();
    expect(mockMutate).not.toHaveBeenCalled();
  });

  it("disables submit button while loading", () => {
    vi.mocked(useLogin).mockReturnValue({
      mutate: mockMutate, isPending: true, error: null,
    } as any);
    render(<LoginForm />, { wrapper: Wrapper });
    expect(screen.getByRole("button", { name: /sign in/i })).toBeDisabled();
  });
});