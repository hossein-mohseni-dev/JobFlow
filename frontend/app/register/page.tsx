"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Brand, Button, Card, Field, Input } from "@/components/ui";
import { api } from "@/lib/api";

const schema = z.object({
  first_name: z.string().min(2),
  last_name: z.string().min(2),
  email: z.string().email(),
  username: z.string().min(3),
  password: z.string().min(8),
});

type FormValues = z.infer<typeof schema>;

export default function RegisterPage() {
  const router = useRouter();
  const form = useForm<FormValues>({ resolver: zodResolver(schema) });
  const onSubmit = form.handleSubmit(async (values) => {
    try {
      await api("/auth/register/", { method: "POST", body: JSON.stringify(values) });
      await api("/auth/login/", { method: "POST", body: JSON.stringify({ username: values.username, password: values.password }) });
      router.push("/verify-email");
    } catch (error) {
      form.setError("root", { message: error instanceof Error ? error.message : "Could not register" });
    }
  });

  return (
    <main className="mx-auto grid min-h-screen max-w-md place-items-center px-4 py-10">
      <Card className="w-full">
        <Brand />
        <h1 className="mt-6 text-2xl font-bold">Create account</h1>
        <form className="mt-5 space-y-4" onSubmit={onSubmit}>
          <div className="grid grid-cols-2 gap-3">
            <Field label="First name"><Input {...form.register("first_name")} /></Field>
            <Field label="Last name"><Input {...form.register("last_name")} /></Field>
          </div>
          <Field label="Email"><Input type="email" {...form.register("email")} /></Field>
          <Field label="Username"><Input {...form.register("username")} /></Field>
          <Field label="Password"><Input type="password" {...form.register("password")} /></Field>
          {form.formState.errors.root ? <p className="text-sm text-rose-600">{form.formState.errors.root.message}</p> : null}
          <Button className="w-full" type="submit">Create account</Button>
        </form>
        <p className="mt-4 text-sm">Already registered? <Link className="text-pine" href="/login">Log in</Link></p>
      </Card>
    </main>
  );
}
