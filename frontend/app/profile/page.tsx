"use client";

import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { Button, Card, Field, Input, Textarea } from "@/components/ui";
import { api } from "@/lib/api";

export default function ProfilePage() {
  const [profile, setProfile] = useState<Record<string, string>>({});
  const [message, setMessage] = useState("");
  const [skill, setSkill] = useState("");
  const [template, setTemplate] = useState("classic");

  useEffect(() => { api<Record<string, string>>("/auth/profile/").then(setProfile); }, []);

  async function downloadCv() {
    const response = await fetch(`/api/v1/auth/profile/cv.pdf?template=${template}`, { credentials: "include" });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `jobflow-cv-${template}.pdf`;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return (
    <Shell>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold">Profile builder</h1>
        <div className="flex gap-2">
          <select aria-label="CV template" className="rounded-xl border px-3" value={template} onChange={(e) => setTemplate(e.target.value)}>
            <option value="classic">Classic</option>
            <option value="modern">Modern</option>
            <option value="compact">Compact</option>
          </select>
          <Button onClick={downloadCv}>Download CV</Button>
        </div>
      </div>
      <Card className="mt-4 grid gap-3 md:grid-cols-2">
        {["first_name", "last_name", "email", "headline", "phone", "city", "website", "linkedin", "github"].map((key) => (
          <Field key={key} label={key.replace("_", " ")}>
            <Input value={profile[key] || ""} onChange={(e) => setProfile({ ...profile, [key]: e.target.value })} />
          </Field>
        ))}
        <div className="md:col-span-2">
          <Field label="Summary"><Textarea rows={4} value={profile.summary || ""} onChange={(e) => setProfile({ ...profile, summary: e.target.value })} /></Field>
        </div>
        <Button onClick={() => api("/auth/profile/", { method: "PUT", body: JSON.stringify(profile) }).then(() => setMessage("Profile saved."))}>Save profile</Button>
      </Card>
      {message ? <p className="mt-3 text-sm text-pine">{message}</p> : null}
      <Card className="mt-4">
        <h2 className="font-bold">Add a skill</h2>
        <div className="mt-3 flex gap-2">
          <Input aria-label="Skill" value={skill} onChange={(e) => setSkill(e.target.value)} placeholder="TypeScript" />
          <Button variant="outline" onClick={() => api("/auth/skills/", { method: "POST", body: JSON.stringify({ name: skill, level: 4 }) }).then(() => setSkill(""))}>Add</Button>
        </div>
      </Card>
    </Shell>
  );
}
