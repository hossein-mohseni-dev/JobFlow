"use client";

import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { Button, Card, Textarea } from "@/components/ui";
import { api } from "@/lib/api";

type Company = { id: number; name: string; industry: string; location: string; about: string; open_roles: number };
type Note = { id: number; company: number; body: string };
type Saved = { id: number; company: Company };

export default function CompaniesPage() {
  const [saved, setSaved] = useState<Saved[]>([]);
  const [all, setAll] = useState<Company[]>([]);
  const [notes, setNotes] = useState<Note[]>([]);
  const [drafts, setDrafts] = useState<Record<number, string>>({});

  async function load() {
    const [savedData, companies, noteData] = await Promise.all([
      api<{ results: Saved[] }>("/saved-companies/?page_size=100"),
      api<{ results: Company[] }>("/companies/?page_size=100"),
      api<{ results: Note[] }>("/notes/?page_size=100"),
    ]);
    setSaved(savedData.results);
    setAll(companies.results);
    setNotes(noteData.results);
  }
  useEffect(() => { load(); }, []);

  return (
    <Shell>
      <h1 className="text-2xl font-bold">Companies and notes</h1>
      <div className="mt-5 grid gap-4 md:grid-cols-2">
        {all.map((company) => (
          <Card key={company.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="text-lg font-bold">{company.name}</h2>
                <p className="text-sm text-ink/60">{company.industry} · {company.location} · {company.open_roles} open roles</p>
              </div>
              <Button variant="outline" onClick={() => api(`/companies/${company.id}/save/`, { method: "POST" }).then(load)}>
                {saved.some((item) => item.company.id === company.id) ? "Saved" : "Save"}
              </Button>
            </div>
            <p className="mt-3 text-sm leading-6">{company.about}</p>
            {notes.filter((note) => note.company === company.id).map((note) => <p key={note.id} className="mt-2 rounded-xl bg-mist px-3 py-2 text-sm">{note.body}</p>)}
            <Textarea className="mt-3" rows={2} aria-label={`Note for ${company.name}`} value={drafts[company.id] || ""} onChange={(e) => setDrafts({ ...drafts, [company.id]: e.target.value })} />
            <Button className="mt-2" variant="outline" onClick={() => api("/notes/", { method: "POST", body: JSON.stringify({ company: company.id, body: drafts[company.id] || "" }) }).then(load)}>Add note</Button>
          </Card>
        ))}
      </div>
    </Shell>
  );
}
