import Link from "next/link";
import { Brand, Button } from "@/components/ui";

export default function HomePage() {
  return (
    <main id="main" className="mx-auto max-w-6xl px-4 py-8">
      <header className="flex items-center justify-between">
        <Brand />
        <div className="flex gap-2">
          <Link href="/login"><Button variant="outline">Log in</Button></Link>
          <Link href="/register"><Button>Create account</Button></Link>
        </div>
      </header>
      <section className="mt-16 grid items-center gap-10 md:grid-cols-2">
        <div>
          <p className="mb-3 text-sm font-medium text-pine">Search, apply, and follow up</p>
          <h1 className="text-4xl font-extrabold leading-tight md:text-5xl">JobFlow keeps every application in one place.</h1>
          <p className="mt-4 max-w-xl text-lg text-ink/70">
            Build a profile, filter roles, save jobs, move a kanban board, schedule interviews, and export a CV.
          </p>
          <div className="mt-6 flex gap-3">
            <Link href="/register"><Button>Start free</Button></Link>
            <Link href="/login"><Button variant="outline">Demo login</Button></Link>
          </div>
          <p className="mt-3 text-sm text-ink/50">Demo account: demo / DemoPass123!</p>
        </div>
        <div className="rounded-3xl border border-white bg-white/80 p-6 shadow-sm">
          {["Applied", "Interview", "Technical Test", "Offer"].map((status, index) => (
            <div key={status} className="mb-3 flex items-center justify-between rounded-2xl bg-mist px-4 py-3">
              <span className="font-medium">{status}</span>
              <span className="text-sm text-ink/50">{index + 2} applications</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
