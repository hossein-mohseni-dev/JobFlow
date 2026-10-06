"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { Badge, Button, Card, Input, Select } from "@/components/ui";
import { api, PLACE_LABELS, TYPE_LABELS } from "@/lib/api";
import { money } from "@/lib/utils";

type Job = {
  id: number;
  title: string;
  location: string;
  employment_type: string;
  workplace: string;
  salary_min: number | null;
  salary_max: number | null;
  currency: string;
  deadline: string | null;
  applied: boolean;
  saved: boolean;
  match_score: number;
  company: { name: string; logo_color: string; industry: string };
};

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [employment, setEmployment] = useState("");
  const [workplace, setWorkplace] = useState("");
  const [error, setError] = useState("");

  async function load(nextPage = page) {
    const params = new URLSearchParams({ page: String(nextPage), page_size: "6" });
    if (search) params.set("search", search);
    if (employment) params.set("employment_type", employment);
    if (workplace) params.set("workplace", workplace);
    const data = await api<{ results: Job[]; count: number }>(`/jobs/?${params.toString()}`);
    setJobs(data.results);
    setCount(data.count);
    setPage(nextPage);
  }

  useEffect(() => {
    load(1).catch((err) => setError(err.message));
  }, []);

  return (
    <Shell>
      <h1 className="text-2xl font-bold">Job search</h1>
      <div className="mt-4 grid gap-3 md:grid-cols-4">
        <Input aria-label="Search jobs" placeholder="Title, company, or skill" value={search} onChange={(e) => setSearch(e.target.value)} />
        <Select aria-label="Employment type" value={employment} onChange={(e) => setEmployment(e.target.value)}>
          <option value="">All types</option>
          <option value="full_time">Full-time</option>
          <option value="part_time">Part-time</option>
          <option value="contract">Contract</option>
          <option value="internship">Internship</option>
        </Select>
        <Select aria-label="Workplace" value={workplace} onChange={(e) => setWorkplace(e.target.value)}>
          <option value="">All workplaces</option>
          <option value="remote">Remote</option>
          <option value="hybrid">Hybrid</option>
          <option value="onsite">Onsite</option>
        </Select>
        <Button onClick={() => load(1).catch((err) => setError(err.message))}>Apply filters</Button>
      </div>
      {error ? <p className="mt-4 text-rose-600">{error}</p> : null}
      <div className="mt-5 grid gap-4">
        {jobs.map((job) => (
          <Card key={job.id} className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
            <div>
              <p className="text-sm text-ink/60">{job.company.name} · {job.company.industry}</p>
              <h2 className="mt-1 text-lg font-bold">{job.title}</h2>
              <div className="mt-2 flex flex-wrap gap-2">
                <Badge>{TYPE_LABELS[job.employment_type]}</Badge>
                <Badge tone="slate">{PLACE_LABELS[job.workplace]}</Badge>
                <Badge tone="amber">Match {job.match_score}</Badge>
                {job.saved ? <Badge>Saved</Badge> : null}
              </div>
              <p className="mt-2 text-sm text-ink/60">{money(job.salary_min, job.currency)} – {money(job.salary_max, job.currency)}</p>
            </div>
            <Link href={`/jobs/${job.id}`}><Button>View role</Button></Link>
          </Card>
        ))}
      </div>
      <div className="mt-4 flex items-center justify-between text-sm">
        <span>{count} roles</span>
        <div className="flex gap-2">
          <Button variant="outline" disabled={page === 1} onClick={() => load(page - 1)}>Previous</Button>
          <Button variant="outline" disabled={page * 6 >= count} onClick={() => load(page + 1)}>Next</Button>
        </div>
      </div>
    </Shell>
  );
}
