"use client";

import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Brand, Button, Card } from "@/components/ui";
import { api } from "@/lib/api";

function VerifyBox() {
  const params = useSearchParams();
  const [message, setMessage] = useState("Paste the token from the verification email, or open the emailed link.");
  const [token, setToken] = useState(params.get("token") || "");
  return (
    <Card>
      <Brand />
      <h1 className="mt-6 text-2xl font-bold">Verify email</h1>
      <p className="mt-2 text-sm text-ink/70">{message}</p>
      <input className="mt-4 w-full rounded-xl border px-3 py-2" aria-label="Verification token" value={token} onChange={(e) => setToken(e.target.value)} />
      <Button className="mt-3" onClick={() => api("/auth/verify-email/", { method: "POST", body: JSON.stringify({ token }) }).then(() => setMessage("Email verified.")).catch((error) => setMessage(error.message))}>Verify</Button>
    </Card>
  );
}

export default function VerifyEmailPage() {
  return <main className="mx-auto grid min-h-screen max-w-md place-items-center px-4"><Suspense><VerifyBox /></Suspense></main>;
}
