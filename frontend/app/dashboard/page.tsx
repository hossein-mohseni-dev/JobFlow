"use client";

import { useEffect, useState } from "react";
import { Bar, BarChart, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Shell } from "@/components/shell";
import { Card } from "@/components/ui";
import { api } from "@/lib/api";

type Stats = {
  totals: { applications: number; saved_companies: number; unread_notifications: number; due_soon: number };
  by_status: { status: string; label: string; total: number }[];
  upcoming_deadlines: { id: number; title: string; company: string; status: string; deadline: string }[];
};
type Rec = { job: { id: number; title: string; company: { name: string } }; analysis: { score: number; recommendation: string } };
type Analytics = {
  applications: number;
  interviews: number;
  offers: number;
  offer_rate: number;
  interview_rate: number;
  win_rate: number;
  saved_jobs: number;
  average_match: number;
  funnel: { stage: string; total: number }[];
  weekly: { week: string; applications: number }[];
  by_company: { company: string; applications: number }[];
};

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [recs, setRecs] = useState<Rec[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    api<Stats>("/dashboard/").then(setStats);
    api<Rec[]>("/recommendations/").then(setRecs);
    api<Analytics>("/analytics/").then(setAnalytics);
  }, []);

  return (
    <Shell>
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="mt-5 grid gap-3 sm:grid-cols-4">
        {[
          ["Applications", stats?.totals.applications],
          ["Interview rate", analytics ? `${Math.round(analytics.interview_rate * 100)}%` : "—"],
          ["Offer rate", analytics ? `${Math.round(analytics.offer_rate * 100)}%` : "—"],
          ["Avg match", analytics?.average_match],
        ].map(([label, value]) => (
          <Card key={String(label)}><p className="text-sm text-ink/60">{label}</p><p className="mt-2 text-3xl font-extrabold">{value ?? "—"}</p></Card>
        ))}
      </div>
      <div className="mt-5 grid gap-4 lg:grid-cols-2">
        <Card>
          <h2 className="mb-4 font-bold">Funnel</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={analytics?.funnel || stats?.by_status || []}>
                <XAxis dataKey={analytics ? "stage" : "label"} tick={{ fontSize: 11 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="total" fill="#0f766e" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
        <Card>
          <h2 className="mb-4 font-bold">Weekly applications</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={analytics?.weekly || []}>
                <XAxis dataKey="week" tick={{ fontSize: 11 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Line type="monotone" dataKey="applications" stroke="#b45309" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        <Card>
          <h2 className="mb-3 font-bold">By company</h2>
          {(analytics?.by_company || []).map((row) => (
            <p key={row.company} className="mb-2 text-sm">{row.company} · {row.applications}</p>
          ))}
          <p className="text-sm text-ink/60">Win rate {analytics ? Math.round(analytics.win_rate * 100) : 0}% · saved jobs {analytics?.saved_jobs ?? 0} · due soon {stats?.totals.due_soon ?? 0}</p>
        </Card>
        <Card>
          <h2 className="mb-3 font-bold">Recommended roles</h2>
          {recs.map((item) => (
            <div key={item.job.id} className="mb-2 rounded-xl bg-mist px-3 py-2 text-sm">
              <p className="font-medium">{item.job.title}</p>
              <p className="text-xs text-ink/60">{item.job.company.name} · score {item.analysis.score}</p>
            </div>
          ))}
        </Card>
      </div>
    </Shell>
  );
}
