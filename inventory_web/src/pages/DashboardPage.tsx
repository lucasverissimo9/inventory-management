import { Button, Container, Group, Text, Title } from "@mantine/core";
import { useAuth } from "@/providers/AuthProvider";

export default function DashboardPage() {
  const { user, logout } = useAuth();

  return (
    <Container py="xl">
      <Group justify="space-between">
        <div>
          <Title order={2}>Dashboard</Title>
          <Text c="dimmed">Welcome, {user?.name}</Text>
        </div>
        <Button variant="subtle" color="red" onClick={logout}>
          Sign out
        </Button>
      </Group>
    </Container>
  );
}