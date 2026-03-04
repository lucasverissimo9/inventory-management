import { useForm } from "@mantine/form";
import {
  Alert, Button, Paper, PasswordInput,
  Stack, Text, TextInput, Title,
} from "@mantine/core";
import { IconAlertCircle } from "@tabler/icons-react";
import { isAxiosError } from "axios";
import { useNavigate, useLocation } from "react-router-dom";
import { useLogin } from "@/features/auth/hooks/useLogin";
import type { ApiErrorResponse, LoginRequest } from "@/features/auth/types";

export const LoginForm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const redirectTo =
    (location.state as { from?: { pathname: string } })?.from?.pathname ?? "/dashboard";

  const { mutate: login, isPending, error } = useLogin();

  const form = useForm<LoginRequest>({
    initialValues: { email: "", password: "" },
    validate: {
      email: (value) => (/\S+@\S+\.\S+/.test(value) ? null : "Enter a valid email"),
      password: (value) => (value.length >= 8 ? null : "At least 8 characters required"),
    },
  });

  const apiErrors = isAxiosError<ApiErrorResponse>(error)
    ? (error.response?.data.errors ?? [])
    : [];
  const globalError = apiErrors.find((e) => !e.field)?.message;

  const handleSubmit = (values: LoginRequest) => {
    login(values, {
      onSuccess: () => navigate(redirectTo, { replace: true }),
    });
  };

  return (
    <Paper radius="md" p="xl" withBorder w={420}>
      <Title order={2} mb={4}>Welcome back</Title>
      <Text c="dimmed" size="sm" mb="lg">Sign in to continue</Text>

      {globalError && (
        <Alert icon={<IconAlertCircle size={16} />} color="red" mb="md" radius="md">
          {globalError}
        </Alert>
      )}

      <form onSubmit={form.onSubmit(handleSubmit)} noValidate>
        <Stack gap="sm">
          <TextInput
            label="Email"
            type="email"
            placeholder="you@example.com"
            {...form.getInputProps("email")}
          />
          <PasswordInput
            label="Password"
            placeholder="Your password"
            {...form.getInputProps("password")}
          />
          <Button type="submit" fullWidth mt="xs" loading={isPending}>
            Sign in
          </Button>
        </Stack>
      </form>
    </Paper>
  );
};