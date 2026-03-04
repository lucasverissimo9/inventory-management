import { Center, Stack, Title } from "@mantine/core";
import { LoginForm } from "@/features/auth/components/LoginForm";

export default function LoginPage() {
  return (
    <Center h="100vh" bg="gray.0">
      <Stack align="center" gap="xl">
        <Title order={1} c="blue">Inventory Management</Title>
        <LoginForm />
      </Stack>
    </Center>
  );
}