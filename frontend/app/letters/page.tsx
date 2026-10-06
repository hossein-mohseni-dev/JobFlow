"use client";

import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { Card, Textarea } from "@/components/ui";
import { api } from "@/lib/api";

type Letter = { id: number; title: string; body: string };

export default function LettersPage() {
  const [letters, setLetters] = useState<Letter[]>([]);
  useEffect(() => { api<{ results: Letter[] }>("/cover-letters/?page_size=50").then((data) => setLetters(data.results)); }, []);
  return (
    <Shell>
      <h1 className="text-2xl font-bold">Cover letters</h1>
      <p className="mt-1 text-sm text-ink/60">Draft one from a job page. Edit the text here.</p>
      <div className="mt-4 space-y-4">
        {letters.map((letter) => (
          <Card key={letter.id}>
            <h2 className="font-bold">{letter.title}</h2>
            <Textarea className="mt-3" rows={8} defaultValue={letter.body} onBlur={(e) => api(`/cover-letters/${letter.id}/`, { method: "PATCH", body: JSON.stringify({ body: e.target.value }) })} />
          </Card>
        ))}
        {!letters.length ? <p className="text-sm text-ink/50">No letters yet.</p> : null}
      </div>
    </Shell>
  );
}
