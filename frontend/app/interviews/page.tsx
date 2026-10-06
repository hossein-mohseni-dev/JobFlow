"use client";

import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { Button, Card, Input, Select } from "@/components/ui";
import { api } from "@/lib/api";

type Interview = { id: number; application: number; kind: string; starts_at: string; location: string; job_title: string; company_name: string };
type Event = { type: string; id: number; title: string; when: string; location: string };
type Application = { id: number; job: { title: string } };

export default function InterviewsPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [apps, setApps] = useState<Application[]>([]);
  const [form, setForm] = useState({ application: "", kind: "video", starts_at: "", location: "" });
  const [message, setMessage] = useState("");

  async function load() {
    setEvents(await api<Event[]>("/calendar/"));
    const data = await api<{ results: Application[] }>("/applications/?page_size=100");
    setApps(data.results);
  }
  useEffect(() => { load().catch((err) => setMessage(err.message)); }, []);

  return (
    <Shell>
      <h1 className="text-2xl font-bold">Interviews and calendar</h1>
      <Card className="mt-4 grid gap-3 md:grid-cols-4">
        <Select aria-label="Application" value={form.application} onChange={(e) => setForm({ ...form, application: e.target.value })}>
          <option value="">Select application</option>
          {apps.map((item) => <option key={item.id} value={item.id}>{item.job.title}</option>)}
        </Select>
        <Select aria-label="Interview type" value={form.kind} onChange={(e) => setForm({ ...form, kind: e.target.value })}>
          <option value="phone">Phone</option>
          <option value="video">Video</option>
          <option value="onsite">Onsite</option>
          <option value="technical">Technical</option>
        </Select>
        <Input aria-label="Start time" type="datetime-local" value={form.starts_at} onChange={(e) => setForm({ ...form, starts_at: e.target.value })} />
        <Button onClick={() => api("/interviews/", { method: "POST", body: JSON.stringify({ ...form, application: Number(form.application), starts_at: new Date(form.starts_at).toISOString() }) }).then(load).catch((err) => setMessage(err.message))}>Schedule</Button>
      </Card>
      {message ? <p className="mt-3 text-sm text-rose-600">{message}</p> : null}
      <div className="mt-4 space-y-3">
        {events.map((event) => (
          <Card key={`${event.type}-${event.id}`}>
            <p className="text-xs uppercase text-pine">{event.type}</p>
            <h2 className="font-bold">{event.title}</h2>
            <p className="text-sm text-ink/60">{String(event.when)} {event.location}</p>
          </Card>
        ))}
      </div>
    </Shell>
  );
}
