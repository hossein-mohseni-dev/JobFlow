"use client";

import { useState } from "react";
import { Brand, Button, Card, Field, Input } from "@/components/ui";
import { api } from "@/lib/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  return (
    <main className="mx-auto grid min-h-screen max-w-md place-items-center px-4">
      <Card className="w-full">
        <Brand />
        <h1 className="mt-6 text-2xl font-bold">Reset password</h1>
        <form className="mt-4 space-y-3" onSubmit={(event) => { event.preventDefault(); api("/auth/password-reset/", { method: "POST", body: JSON.stringify({ email }) }).then(() => setMessage("If the account exists, check the server email log.")); }}>
          <Field label="Email"><Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /></Field>
          <Button type="submit">Send reset link</Button>
        </form>
        {message ? <p className="mt-3 text-sm text-pine">{message}</p> : null}
      </Card>
    </main>
  );
}
