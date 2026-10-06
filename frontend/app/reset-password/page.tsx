"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { Suspense, useState } from "react";
import { Brand, Button, Card, Field, Input } from "@/components/ui";
import { api } from "@/lib/api";

function ResetForm() {
  const params = useSearchParams();
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  return (
    <Card className="w-full">
      <Brand />
      <h1 className="mt-6 text-2xl font-bold">Choose a new password</h1>
      <form className="mt-4 space-y-3" onSubmit={(event) => {
        event.preventDefault();
        api("/auth/password-reset/confirm/", { method: "POST", body: JSON.stringify({ token: params.get("token"), password }) })
          .then(() => router.push("/login"))
          .catch((error) => setMessage(error.message));
      }}>
        <Field label="New password"><Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} minLength={8} required /></Field>
        <Button type="submit">Update password</Button>
      </form>
      {message ? <p className="mt-3 text-sm text-rose-600">{message}</p> : null}
    </Card>
  );
}

export default function ResetPasswordPage() {
  return <main className="mx-auto grid min-h-screen max-w-md place-items-center px-4"><Suspense><ResetForm /></Suspense></main>;
}
