"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Brand, Button, Card, Field, Input } from "@/components/ui";
import { api } from "@/lib/api";

const schema = z.object({
  username: z.string().min(3, "At least 3 characters"),
  password: z.string().min(8, "At least 8 characters"),
});

type FormValues = z.infer<typeof schema>;

export default function LoginPage() {
  const router = useRouter();
  const form = useForm<FormValues>({ resolver: zodResolver(schema), defaultValues: { username: "demo", password: "DemoPass123!" } });
  const onSubmit = form.handleSubmit(async (values) => {
    try {
      await api("/auth/login/", { method: "POST", body: JSON.stringify(values) });
      router.push("/dashboard");
    } catch (error) {
      form.setError("root", { message: error instanceof Error ? error.message : "Login failed" });
    }
  });

  return (
    <main className="mx-auto grid min-h-screen max-w-md place-items-center px-4">
      <Card className="w-full">
        <Brand />
        <h1 className="mt-6 text-2xl font-bold">Log in</h1>
        <form className="mt-5 space-y-4" onSubmit={onSubmit}>
          <Field label="Username" error={form.formState.errors.username?.message}><Input autoComplete="username" {...form.register("username")} /></Field>
          <Field label="Password" error={form.formState.errors.password?.message}><Input type="password" autoComplete="current-password" {...form.register("password")} /></Field>
          {form.formState.errors.root ? <p className="text-sm text-rose-600">{form.formState.errors.root.message}</p> : null}
          <Button className="w-full" type="submit">Continue</Button>
        </form>
        <p className="mt-4 text-sm"><Link className="text-pine" href="/forgot-password">Forgot password</Link></p>
        <p className="mt-2 text-sm text-ink/60">New here? <Link className="text-pine" href="/register">Create an account</Link></p>
      </Card>
    </main>
  );
}
