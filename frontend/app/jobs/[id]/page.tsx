"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { Badge, Button, Card, Textarea } from "@/components/ui";
import { api, PLACE_LABELS, TYPE_LABELS } from "@/lib/api";

type Job = {
  id: number;
  title: string;
  location: string;
  employment_type: string;
  workplace: string;
  description: string;
  requirements: string;
  tags: string;
  deadline: string | null;
  applied: boolean;
  saved: boolean;
  match_score: number;
  company: { id: number; name: string; about: string; industry: string };
};
type Analysis = { score: number; matched_skills: string[]; missing_skills: string[]; summary: string; recommendation: string };

export default function JobDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const [job, setJob] = useState<Job | null>(null);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [note, setNote] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    api<Job>(`/jobs/${params.id}/`).then(setJob).catch((err) => setMessage(err.message));
    api<Analysis>(`/jobs/${params.id}/analyze/`).then(setAnalysis).catch(() => undefined);
  }, [params.id]);

  if (!job) return <Shell><p>{message || "Loading..."}</p></Shell>;

  return (
    <Shell>
      <Card>
        <p className="text-sm text-pine">{job.company.name} · {job.company.industry}</p>
        <h1 className="mt-1 text-3xl font-extrabold">{job.title}</h1>
        <div className="mt-3 flex flex-wrap gap-2">
          <Badge>{TYPE_LABELS[job.employment_type]}</Badge>
          <Badge tone="slate">{PLACE_LABELS[job.workplace]}</Badge>
          <Badge tone="amber">Match {job.match_score}</Badge>
        </div>
        <p className="mt-5 leading-7">{job.description}</p>
        <h2 className="mt-6 font-bold">Requirements</h2>
        <p className="mt-2 leading-7">{job.requirements}</p>
        {analysis ? (
          <div className="mt-5 rounded-2xl bg-mist p-4">
            <h2 className="font-bold">AI job analysis</h2>
            <p className="mt-2 text-sm">{analysis.summary}</p>
            <p className="mt-2 text-sm">{analysis.recommendation}</p>
            <p className="mt-2 text-xs">Matched: {analysis.matched_skills.join(", ") || "none"} · Missing: {analysis.missing_skills.join(", ") || "none"}</p>
          </div>
        ) : null}
        <Textarea className="mt-5" rows={4} aria-label="Application note" placeholder="Application note" value={note} onChange={(e) => setNote(e.target.value)} />
        <div className="mt-4 flex flex-wrap gap-2">
          <Button disabled={job.applied} onClick={() => api("/applications/", { method: "POST", body: JSON.stringify({ job_id: job.id, note }) }).then(() => router.push("/applications")).catch((err) => setMessage(err.message))}>
            {job.applied ? "Already applied" : "Apply"}
          </Button>
          <Button variant="outline" onClick={() => api(`/jobs/${job.id}/save/`, { method: "POST" }).then(() => setMessage("Job saved."))}>Save job</Button>
          <Button variant="outline" onClick={() => api(`/companies/${job.company.id}/save/`, { method: "POST" }).then(() => setMessage("Company saved."))}>Save company</Button>
          <Button variant="outline" onClick={() => api("/cover-letters/draft/", { method: "POST", body: JSON.stringify({ job_id: job.id }) }).then(() => router.push("/letters"))}>Draft cover letter</Button>
        </div>
        {message ? <p className="mt-3 text-sm text-pine">{message}</p> : null}
      </Card>
    </Shell>
  );
}
