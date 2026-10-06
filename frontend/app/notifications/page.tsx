"use client";

import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { Button, Card } from "@/components/ui";
import { api } from "@/lib/api";

type Note = { id: number; title: string; body: string; is_read: boolean; created_at: string };

export default function NotificationsPage() {
  const [items, setItems] = useState<Note[]>([]);
  async function load() {
    const data = await api<{ results: Note[] }>("/notifications/?page_size=100");
    setItems(data.results);
  }
  useEffect(() => { load(); }, []);
  return (
    <Shell>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Notifications</h1>
        <Button variant="outline" onClick={() => api("/notifications/read/", { method: "POST" }).then(load)}>Mark all read</Button>
      </div>
      <div className="mt-4 space-y-3">
        {items.map((item) => (
          <Card key={item.id} className={item.is_read ? "opacity-70" : ""}>
            <h2 className="font-bold">{item.title}</h2>
            <p className="mt-1 text-sm">{item.body}</p>
            {!item.is_read ? <Button className="mt-2" variant="ghost" onClick={() => api(`/notifications/${item.id}/read/`, { method: "POST" }).then(load)}>Mark read</Button> : null}
          </Card>
        ))}
      </div>
    </Shell>
  );
}
