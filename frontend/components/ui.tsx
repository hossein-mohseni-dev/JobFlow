import Link from "next/link";
import { cn } from "@/lib/utils";

export function Button({
  className,
  variant = "primary",
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "ghost" | "outline" }) {
  const styles = {
    primary: "bg-pine text-white hover:bg-teal-800",
    ghost: "bg-transparent hover:bg-sand text-ink",
    outline: "border border-teal-900/15 bg-white hover:bg-sand",
  };
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2 text-sm font-medium transition disabled:opacity-50",
        styles[variant],
        className
      )}
      {...props}
    />
  );
}

export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className="w-full rounded-xl border border-teal-900/10 bg-white px-3 py-2 text-sm outline-none ring-pine/30 focus:ring-2"
      {...props}
    />
  );
}

export function Textarea(props: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className="w-full rounded-xl border border-teal-900/10 bg-white px-3 py-2 text-sm outline-none ring-pine/30 focus:ring-2"
      {...props}
    />
  );
}

export function Select(props: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className="w-full rounded-xl border border-teal-900/10 bg-white px-3 py-2 text-sm outline-none ring-pine/30 focus:ring-2"
      {...props}
    />
  );
}

export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("rounded-2xl border border-white/70 bg-white/90 p-5 shadow-sm", className)} {...props} />;
}

export function Badge({ children, tone = "teal" }: { children: React.ReactNode; tone?: "teal" | "amber" | "rose" | "slate" }) {
  const tones = {
    teal: "bg-teal-50 text-teal-800",
    amber: "bg-amber-50 text-amber-800",
    rose: "bg-rose-50 text-rose-800",
    slate: "bg-slate-100 text-slate-700",
  };
  return <span className={cn("rounded-full px-2.5 py-1 text-xs font-medium", tones[tone])}>{children}</span>;
}

export function Field({ label, error, children }: { label: string; error?: string; children: React.ReactNode }) {
  return (
    <label className="block space-y-1.5 text-sm">
      <span className="font-medium text-ink/80">{label}</span>
      {children}
      {error ? <span className="text-xs text-rose-600">{error}</span> : null}
    </label>
  );
}

export function Brand() {
  return (
    <Link href="/" className="flex items-center gap-2 font-extrabold tracking-tight">
      <span className="grid h-9 w-9 place-items-center rounded-xl bg-pine text-white">JF</span>
      JobFlow
    </Link>
  );
}
