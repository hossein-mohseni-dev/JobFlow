"use client";

import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { Card, Select, Textarea } from "@/components/ui";
import { api, STATUS_LABELS } from "@/lib/api";

type Application = {
  id: number;
  status: string;
  note: string;
  deadline: string | null;
  job: { title: string; company: { name: string } };
};

const columns = Object.keys(STATUS_LABELS);

export default function ApplicationsPage() {
  const [items, setItems] = useState<Application[]>([]);
  const [error, setError] = useState("");
  const [dragging, setDragging] = useState<number | null>(null);

  async function load() {
    const data = await api<{ results: Application[] }>("/applications/?page_size=100");
    setItems(data.results);
  }
  useEffect(() => {
    load().catch((err) => setError(err.message));
  }, []);

  async function update(id: number, payload: Partial<Application>) {
    setItems((current) => current.map((item) => (item.id === id ? { ...item, ...payload } : item)));
    await api(`/applications/${id}/`, { method: "PATCH", body: JSON.stringify(payload) });
  }

  return (
    <Shell>
      <h1 className="text-2xl font-bold">Application kanban</h1>
      <p className="mt-1 text-sm text-ink/60">Drag a card into Applied, Interview, Technical Test, Offer, or Rejected.</p>
      {error ? <p className="mt-3 text-rose-600">{error}</p> : null}
      <div className="mt-5 grid gap-3 overflow-x-auto xl:grid-cols-5">
        {columns.map((status) => (
          <section
            key={status}
            aria-label={STATUS_LABELS[status]}
            className="min-h-64 min-w-[220px] rounded-2xl bg-white/70 p-3"
            onDragOver={(event) => event.preventDefault()}
            onDrop={(event) => {
              event.preventDefault();
              const id = Number(event.dataTransfer.getData("text/plain"));
              if (id) update(id, { status }).catch((err) => setError(err.message));
              setDragging(null);
            }}
          >
            <h2 className="mb-3 text-sm font-bold">{STATUS_LABELS[status]}</h2>
            {items.filter((item) => item.status === status).map((item) => (
              <Card
                key={item.id}
                draggable
                onDragStart={(event) => {
                  event.dataTransfer.setData("text/plain", String(item.id));
                  event.dataTransfer.effectAllowed = "move";
                  setDragging(item.id);
                }}
                onDragEnd={() => setDragging(null)}
                className={`mb-3 cursor-grab p-3 active:cursor-grabbing ${dragging === item.id ? "opacity-50" : ""}`}
              >
                <p className="font-medium">{item.job.title}</p>
                <p className="text-xs text-ink/50">{item.job.company.name}</p>
                <Select className="mt-2" aria-label={`Status for ${item.job.title}`} value={item.status} onChange={(e) => update(item.id, { status: e.target.value }).catch((err) => setError(err.message))}>
                  {columns.map((option) => <option key={option} value={option}>{STATUS_LABELS[option]}</option>)}
                </Select>
                <label className="mt-2 block text-xs">Deadline
                  <input className="mt-1 w-full rounded-lg border px-2 py-1" type="date" value={item.deadline || ""} onChange={(e) => update(item.id, { deadline: e.target.value }).catch((err) => setError(err.message))} />
                </label>
                <Textarea className="mt-2" rows={2} aria-label={`Note for ${item.job.title}`} defaultValue={item.note} onBlur={(e) => update(item.id, { note: e.target.value })} />
              </Card>
            ))}
          </section>
        ))}
      </div>
    </Shell>
  );
}
